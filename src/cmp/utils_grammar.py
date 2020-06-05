import cmp.pycompiler
from queue import Queue
from random import randint
from cmp.automata import *
from cmp.pycompiler import *
from cmp.type_check import type_check

class UtilsGrammar:

    epsilon = 'ε'
    # epsilon = 'e'

    @type_check
    def GetGrammar(text : str) -> Grammar:
        """
        Transforma un string en este formato S -> a S b | epsilon 
        a un objeto Grammar.
        """
        terminals = []
        nonTerminals = []
        productions = []

        try:
            lines = text.split('\n')

            for line in lines:
                head,bodies = line.split('->')

                head, = head.split()
                nonTerminals.append(head)

                for body in bodies.split('|'):
                    productions.append({'Head': head, 'Body': list(body.split())})
                    terminals.extend(productions[-1]['Body'])

        except:
            raise BadTextFormatException()

        sterminals = set(terminals).difference(nonTerminals + ['epsilon'])
        snonTerminals = set(nonTerminals)

        data = json.dumps({
                            'NonTerminals': [nt for nt in nonTerminals if nt in snonTerminals and snonTerminals.discard(nt) is None],
                            'Terminals': [t for t in terminals if t in sterminals and sterminals.discard(t) is None],
                            'Productions': productions
                        })

        return Grammar.FromJson(data)

    @type_check
    def CloneGrammar(grammar : Grammar) -> cmp.pycompiler.Grammar:
        
        grammar_clone = Grammar()
        symbols = {nonTerminal : grammar_clone.NonTerminal(nonTerminal.Name,
            nonTerminal == grammar.startSymbol) for nonTerminal in grammar.nonTerminals}
        symbols.update({terminal : grammar_clone.Terminal(terminal.Name)
            for terminal in grammar.terminals})
        
        for production in grammar.Productions:
            x = symbols[production.Left]
            if isinstance(production.Right, Epsilon):
                x %= grammar_clone.Epsilon
            else:
                x %= Sentence(*[symbols[symbol] for symbol in production.Right])

        return grammar_clone

    @type_check
    def IsNotNull(grammar : Grammar) -> tuple:
        """
        Chequea si la gramatica genera el lenguaje vacio, si no lo
        genera devuelve ademas un conjunto con los simbolos usados.
        """
        accepted = set()
        visited = set()

        def DFS(symbol):
            visited.add(symbol)
            acc = False

            if isinstance(symbol, Terminal):
                acc = True
            else:
                for production in symbol.productions:
                    for s in production.Right:
                        if s not in visited:
                            DFS(s)
                    acc |= all(s in accepted for s in production.Right)

            if acc:
                accepted.add(symbol)

        DFS(grammar.startSymbol)
        pending = Queue()
        if grammar.startSymbol in accepted:
            pending.put(grammar.startSymbol)
        visited = set()

        while not pending.empty():
            symbol = pending.get()
            visited.add(symbol)

            if isinstance(symbol, NonTerminal):
                for production in symbol.productions:
                    if all(s in accepted for s in production.Right):
                        for s in production.Right:
                            if s not in visited:
                                pending.put(s)

        is_not_null = grammar.startSymbol in accepted
        return is_not_null, visited

    @type_check
    def RemoveUnnecessaryProductions(G : Grammar, keep_symbols) -> None:
        """
        Elimina las producciones innecesarias de la gramatica.
        """
        G.Productions = []
        G.nonTerminals = [nonTerminal for nonTerminal in G.nonTerminals
            if nonTerminal in keep_symbols]
        G.terminals = [terminal for terminal in G.terminals
            if terminal in keep_symbols]

        for non_terminal in G.nonTerminals:
            productions = non_terminal.productions.copy()
            non_terminal.productions = []

            for production in productions:
                if all(symbol in keep_symbols for symbol in production.Right):
                    non_terminal %= production.Right

    @type_check
    def RemoveLeftRecursion(G : Grammar) -> None:
        """
        Elimina la recursion izquierda inmediata de la gramatica.
        """
        G.Productions = []
        nonTerminals = G.nonTerminals.copy()

        for non_terminal in nonTerminals:
            recursion = [prod.Right[1:] for prod in non_terminal.productions
                if len(prod.Right) > 0 and prod.Right[0] == non_terminal]
            no_recursion = [prod.Right for prod in non_terminal.productions
                if len(prod.Right) == 0 or prod.Right[0] != non_terminal]

            if len(recursion) > 0:
                new_non_terminal = UtilsGrammar.GetNewNonTerminal(nonTerminals, non_terminal.Name)
                non_terminal.productions = []
                aux = G.NonTerminal(new_non_terminal)

                for prod in no_recursion:
                    non_terminal %= Sentence(*prod) + aux

                for prod in recursion:
                    aux %= Sentence(*prod) + aux

                aux %= G.Epsilon
            else:
                G.Productions.extend(non_terminal.productions)
    
    @type_check
    def GetNewNonTerminal(nonTerminals : list, non_terminal : str) -> str:
        """
        Devuelve un nuevo non-terminal que no se encuentra dentro de
        los non-terminales de la gramatica y cuyo prefijo es el parametro
        non_terminal.
        """

        while True:

            rand = randint(0, 9)
            new_non_terminal = non_terminal + str(rand)

            if not nonTerminals.__contains__(new_non_terminal):
                return new_non_terminal

    @type_check
    def RemoveCommonPrefix(G : Grammar) -> None:
        """
        Elimina los prefijos comunes de la gramatica.
        """
        G.Productions = []
        pending = Queue()

        for non_terminal in G.nonTerminals:
            pending.put(non_terminal)

        while not pending.empty():
            nonTerminal = pending.get()
            productions = nonTerminal.productions.copy()
            nonTerminal.productions = []
            visited = set()

            for i,p in enumerate(productions):
                if p not in visited:
                    n = len(p.Right)
                    same_prefix = []

                    for p2 in productions[i:]:
                        m = 0

                        for s1, s2 in zip(p.Right, p2.Right):
                            if s1 == s2:
                                m += 1
                            else:
                                break
                        
                        if m > 0:
                            same_prefix.append(p2)
                            n = min(n, m)

                    if len(same_prefix) > 1:
                        visited.update(same_prefix)
                        new_non_terminal = UtilsGrammar.GetNewNonTerminal(G.nonTerminals, nonTerminal.Name)
                        aux = G.NonTerminal(new_non_terminal)

                        nonTerminal %= Sentence(*p.Right[:n]) + aux
                        for p2 in same_prefix:
                            if n == len(p2.Right):
                                aux %= G.Epsilon
                            else:
                                aux %= Sentence(*p2.Right[n:])

                        pending.put(aux)
                    else:
                        visited.add(p)
                        nonTerminal %= p.Right
    
    @type_check
    def BuildAutomaton(G : Grammar) -> tuple:
        """
        Construye un automata finito para una gramatica regular.
        """
        states = { nonTerminal: State(nonTerminal.Name) for nonTerminal in G.nonTerminals }
        final_state = State('F\'', True)

        start_in_right = False
        epsilon_production = False

        for nonTerminal in G.nonTerminals:
            for production in nonTerminal.productions:
                right = production.Right

                if isinstance(right, Epsilon) and nonTerminal == G.startSymbol:
                    epsilon_production = True
                    continue
                    
                start_in_right |= G.startSymbol in right
                n = len(right)

                # X -> w
                if n == 1 and isinstance(right[0], Terminal):
                    states[nonTerminal].add_transition(right[0].Name, final_state)
                    continue

                # X -> w Y
                if n == 2 and isinstance(right[0], Terminal) and isinstance(right[1], NonTerminal):
                    states[nonTerminal].add_transition(right[0].Name, states[right[1]])
                    continue

                return states[G.startSymbol], False

        states[G.startSymbol].final = epsilon_production
        return states[G.startSymbol], not (start_in_right and epsilon_production)

    @type_check
    def RegularExpressionUnion(reg_exp1, reg_exp2):

        if reg_exp1 is None:
            return reg_exp2

        if reg_exp2 is None:
            return reg_exp1

        if reg_exp1 == reg_exp2:
            return reg_exp1

        return f'({reg_exp1}|{reg_exp2})'

    @type_check
    def RegularExpressionConcat(reg_exp1, reg_exp2):
        if reg_exp1 is None or reg_exp2 is None:
            return None

        if reg_exp1 is UtilsGrammar.epsilon:
            return reg_exp2

        if reg_exp2 is UtilsGrammar.epsilon:
            return reg_exp1

        return f'{reg_exp1}{reg_exp2}'

    @type_check
    def RegularExpressionStar(reg_exp):
        if reg_exp is None or reg_exp is UtilsGrammar.epsilon:
            return reg_exp

        return f'({reg_exp})*'

    @type_check
    def GetRegularExpression(automaton : cmp.automata.State):
        """
        Construye una expresion regular a partir de un automata finito
        no determinista.
        """
        states = list(automaton)
        states_index = {state: i for i, state in enumerate(states)}
        n = len(states)

        dp = [[[None for k in range(n + 1)] for j in range(n)] for i in range(n)]

        for i in range(n):
            dp[i][i][0] = UtilsGrammar.epsilon

        for i, state in enumerate(states):
            for symbol, transitions in state.transitions.items():
                for state2 in transitions:
                    j = states_index[state2]
                    dp[i][j][0] = UtilsGrammar.RegularExpressionUnion(dp[i][j][0], symbol)

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dp[i][j][k + 1] = UtilsGrammar.RegularExpressionUnion(dp[i][j][k], 
                        UtilsGrammar.RegularExpressionConcat(dp[i][k][k], 
                            UtilsGrammar.RegularExpressionConcat(UtilsGrammar.RegularExpressionStar(dp[k][k][k]),
                                dp[k][j][k])))

        reg_exp = None
        for i in range(n):
            if states[i].final:
                reg_exp = UtilsGrammar.RegularExpressionUnion(reg_exp, dp[0][i][n])

        return reg_exp

class BadTextFormatException(Exception):
    """
    Class for wrong format in texts
    used to convert to a grammar
    """
    pass