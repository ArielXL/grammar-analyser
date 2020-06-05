from cmp.automata import *
from cmp.pycompiler import *
from cmp.utils import ContainerSet
from cmp.type_check import type_check

class UtilsParsers:

    @type_check
    def ComputeLocalFirst(firsts : dict, alpha) -> ContainerSet:
        """
        Computa el conjunto First de la cadena alpha, esta cadena puede 
        tener tanto terminales como non-terminales.
        """
        first_alpha = ContainerSet()
        
        try:
            alpha_is_epsilon = alpha.IsEpsilon
        except:
            alpha_is_epsilon = False

        # alpha == epsilon ? First(alpha) = { epsilon }
        if alpha_is_epsilon:
            first_alpha.set_epsilon()

        # alpha = X1 ... XN
        # First(Xi) subset of First(alpha)
        # epsilon  in First(X1)...First(Xi) ? First(Xi+1) subset of First(X) & First(alpha)
        # epsilon in First(X1)...First(XN) ? epsilon in First(X) & First(alpha)
        else:
            for symbol in alpha:
                first_symbol = firsts[symbol]
                first_alpha.update(first_symbol)
                if not first_symbol.contains_epsilon:
                    break
            else:
                first_alpha.set_epsilon()

        return first_alpha

    @type_check
    def ComputeFirsts(G : Grammar) -> dict:
        """
        Calcula el conjunto First de los terminales, los no-terminales
        y las partes derechas de la gramatica.
        """
        firsts = {}
        change = True
        
        # init First(Vt)
        for terminal in G.terminals:
            firsts[terminal] = ContainerSet(terminal)
            
        # init First(Vn)
        for nonterminal in G.nonTerminals:
            firsts[nonterminal] = ContainerSet()
        
        while change:
            change = False
            
            # P: X -> alpha
            for production in G.Productions:
                X = production.Left
                alpha = production.Right
                
                # get current First(X)
                first_X = firsts[X]
                    
                # init First(alpha)
                try:
                    first_alpha = firsts[alpha]
                except:
                    first_alpha = firsts[alpha] = ContainerSet()
                
                # CurrentFirst(alpha)???
                local_first = UtilsParsers.ComputeLocalFirst(firsts, alpha)
                
                # update First(X) and First(alpha) from CurrentFirst(alpha)
                change |= first_alpha.hard_update(local_first)
                change |= first_X.hard_update(local_first)
                        
        # First(Vt) + First(Vt) + First(RightSides)
        return firsts

    @type_check
    def ComputeFollows(G: Grammar, firsts : dict) -> dict:
        """
        Calcula el conjunto Follow de todos los no terminales de la
        gramatica.
        """
        follows = { }
        change = True
        local_firsts = {}
        
        # init Follow(Vn)
        for nonterminal in G.nonTerminals:
            follows[nonterminal] = ContainerSet()
        follows[G.startSymbol] = ContainerSet(G.EOF)
        
        while change:
            change = False
            
            # P: X -> alpha
            for production in G.Productions:
                X = production.Left
                alpha = production.Right
                
                follow_X = follows[X]
                
                # X -> zeta Y beta
                # First(beta) - { epsilon } subset of Follow(Y)
                # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
                for i, symbol in enumerate(alpha):
                    if symbol.IsNonTerminal:
                        follow_symbol = follows[symbol]
                        beta = alpha[i + 1:]
                        try:
                            first_beta = local_firsts[beta]
                        except KeyError:
                            first_beta = local_firsts[beta] = UtilsParsers.ComputeLocalFirst(firsts, beta)
                        change |= follow_symbol.update(first_beta)
                        if first_beta.contains_epsilon or len(beta) == 0:
                            change |= follow_symbol.update(follow_X)
        
        return follows

    @type_check
    def Register(table : dict, state, symbol, value) -> bool:

        if state not in table:
            table[state] = dict()

        row = table[state]
        
        if symbol not in row:
            row[symbol] = []

        cell = row[symbol]

        if value not in cell:
            cell.append(value)

        return len(cell) == 1

    def Tokenizer(G : Grammar, w : list):
        return [G[word] for word in w.split()] + [G.EOF]

