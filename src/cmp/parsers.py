from cmp.automata import *
from cmp.pycompiler import *
from cmp.utils import ContainerSet
from cmp.type_check import type_check
from cmp.utils_grammar import UtilsGrammar
from cmp.utils_parsers import UtilsParsers

class LL1Parser:

    @type_check
    def Build_LL1_Table(G : Grammar, firsts : dict, follows : dict) -> tuple:
        """
        Computa la tabla del parser LL(1).
        """
        # init parsing table
        M = {}
        is_ll1 = True
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            # working with symbols on First(alpha) ...
            first_alpha = firsts[alpha]
            for symbol in first_alpha:
                is_ll1 &= UtilsParsers.Register(M, X, symbol, production)
            
            # working with epsilon...
            if first_alpha.contains_epsilon:
                for symbol in follows[X]:
                    is_ll1 &= UtilsParsers.Register(M, X, symbol, production)
            
        # parsing table is ready!!!
        return M, is_ll1

    @type_check
    def NonRecursivePredictiveMethod(G : Grammar, M : dict, firsts : dict, follows : dict):
        
        # parser construction...
        def parser(w):    
            # w ends with $ (G.EOF)
            # init:
            stack = [G.startSymbol]
            cursor = 0
            output = []
            
            # parsing w...
            while stack:
                top = stack.pop()
                a = w[cursor]
                
                if top.IsTerminal:
                    if top == a:
                        cursor += 1
                    else:
                        return None
                else:
                    try:
                        production = M[top][a][0]
                    except KeyError:
                        return None

                    output.append(production)
                    stack.extend(reversed(production.Right))
            
            # left parse is ready!!!
            return output
        
        # parser is ready!!!
        return parser

class Action(tuple):

    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __str__(self):
        try:
            action, tag = self
            return f"{'S' if action == Action.SHIFT else 'OK' if action == Action.OK else ''}{tag}"
        except:
            return str(tuple(self))

    __repr__ = __str__

class ShiftReduceParser:
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self.BuildParsingTable()
    
    def BuildParsingTable(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, w[cursor:])
                
            # (Detect error)
            try:
                action, tag = self.action[state][lookahead][0]
                # (Shift case)
                if action == Action.SHIFT:
                    stack.append(tag)
                    cursor += 1
                # (Reduce case)
                elif action == Action.REDUCE:
                    for _ in range(len(tag.Right)): stack.pop()
                    stack.append(self.goto[stack[-1]][tag.Left][0])
                    output.append(tag)
                # (OK case)
                elif action == Action.OK:
                    output.reverse()
                    return output
                # (Invalid case)
                else:
                    assert False, 'Must be something wrong!'
            except KeyError:
                return None

class SLR1Parser(ShiftReduceParser):
    
    def BuildAutomatonLR0(self):
        G = self.augmentedG = self.G.AugmentedGrammar(True)

        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0)

        automaton = State(start_item, True)

        pending = [ start_item ]
        visited = { start_item: automaton }

        while pending:
            current_item = pending.pop()
            if current_item.IsReduceItem:
                continue
            
            # (Decide which transitions to add)
            next_symbol = current_item.NextSymbol
            
            next_item = current_item.NextItem()
            if not next_item in visited:
                pending.append(next_item)
                visited[next_item] = State(next_item, True)
            
            if next_symbol.IsNonTerminal:
                for prod in next_symbol.productions:
                        next_item = Item(prod, 0)
                        if not next_item in visited:
                            pending.append(next_item)
                            visited[next_item] = State(next_item, True) 

            current_state = visited[current_item]
            
            # (Add the decided transitions)
            current_state.add_transition(next_symbol.Name, visited[current_item.NextItem()])
            
            if next_symbol.IsNonTerminal:
                for prod in next_symbol.productions:
                        current_state.add_epsilon_transition(visited[Item(prod, 0)])
            
        self.automaton = automaton.to_deterministic(empty_formatter)

    def BuildParsingTable(self):
        self.is_slr1 = True
        self.BuildAutomatonLR0()

        firsts = UtilsParsers.ComputeFirsts(self.augmentedG)
        follows = UtilsParsers.ComputeFollows(self.augmentedG, firsts)
        
        for i, node in enumerate(self.automaton):
            if self.verbose: print(i, node)
            node.idx = i
            node.tag = f'I{i}'

        for node in self.automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == self.augmentedG.startSymbol:
                        self.is_slr1 &= UtilsParsers.Register(self.action, idx, self.augmentedG.EOF, Action((Action.OK, '')))
                    else:
                        for symbol in follows[prod.Left]:
                            self.is_slr1 &= UtilsParsers.Register(self.action, idx, symbol, Action((Action.REDUCE, prod)))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.is_slr1 &= UtilsParsers.Register(self.action, idx, next_symbol, Action((Action.SHIFT, node[next_symbol.Name][0].idx)))
                    else:
                        self.is_slr1 &= UtilsParsers.Register(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)

class LR1Parser(ShiftReduceParser):

    def Expand(item, firsts):
        next_symbol = item.NextSymbol
        if next_symbol is None or not next_symbol.IsNonTerminal:
            return []
        
        lookaheads = ContainerSet()
        # (Compute lookahead for child items)
        for preview in item.Preview():
            lookaheads.hard_update(UtilsParsers.ComputeLocalFirst(firsts, preview))
        
        assert not lookaheads.contains_epsilon
        # (Build and return child items)
        return [Item(prod, 0, lookaheads) for prod in next_symbol.productions]

    def Compress(items):
        centers = {}

        for item in items:
            center = item.Center()
            try:
                lookaheads = centers[center]
            except KeyError:
                centers[center] = lookaheads = set()
            lookaheads.update(item.lookaheads)
        
        return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

    def ClosureLR1(items, firsts):
        closure = ContainerSet(*items)
        
        changed = True
        while changed:
            changed = False
            
            new_items = ContainerSet()
            for item in closure:
                new_items.extend(LR1Parser.Expand(item, firsts))

            changed = closure.update(new_items)
            
        return LR1Parser.Compress(closure)
    
    def GotoLR1(items, symbol, firsts=None, just_kernel=False):
        assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
        items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
        return items if just_kernel else LR1Parser.ClosureLR1(items, firsts)

    def BuildAutomatonLR1(self):
        G = self.augmentedG = self.G.AugmentedGrammar(True)

        firsts = UtilsParsers.ComputeFirsts(G)
        firsts[G.EOF] = ContainerSet(G.EOF)
        
        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0, lookaheads=(G.EOF,))
        start = frozenset([start_item])
        
        closure = LR1Parser.ClosureLR1(start, firsts)
        automaton = State(frozenset(closure), True)
        
        pending = [ start ]
        visited = { start: automaton }
        
        while pending:
            current = pending.pop()
            current_state = visited[current]
            
            for symbol in G.terminals + G.nonTerminals:
                # (Get/Build `next_state`)
                kernels = LR1Parser.GotoLR1(current_state.state, symbol, just_kernel=True)
                
                if not kernels:
                    continue
                
                try:
                    next_state = visited[kernels]
                except KeyError:
                    pending.append(kernels)
                    visited[pending[-1]] = next_state = State(frozenset(LR1Parser.GotoLR1(current_state.state, symbol, firsts)), True)
                
                current_state.add_transition(symbol.Name, next_state)
        
        automaton.set_formatter(empty_formatter)
        self.automaton = automaton

    def BuildParsingTable(self):
        self.is_lr1 = True
        self.BuildAutomatonLR1()
        
        for i, node in enumerate(self.automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
            node.tag = f'I{i}'

        for node in self.automaton:
            idx = node.idx
            for item in node.state:
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == self.augmentedG.startSymbol:
                        self.is_lr1 &= UtilsParsers.Register(self.action, idx, self.augmentedG.EOF, Action((Action.OK, '')))
                    else:
                        for lookahead in item.lookaheads:
                            self.is_lr1 &= UtilsParsers.Register(self.action, idx, lookahead, Action((Action.REDUCE, prod)))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self.is_lr1 &= UtilsParsers.Register(self.action, idx, next_symbol, Action((Action.SHIFT, node[next_symbol.Name][0].idx)))
                    else:
                        self.is_lr1 &= UtilsParsers.Register(self.goto, idx, next_symbol, node[next_symbol.Name][0].idx)
                pass

class LALRParser(LR1Parser):

    def MergueItemsLookaheads(items, others):
        if len(items) != len(others):
            return False

        new_lookaheads = []
        for item in items:
            for item2 in others:
                if item.Center() == item2.Center():
                    new_lookaheads.append(item2.lookaheads)
                    break
            else:
                return False

        for item, new_lookahead in zip(items, new_lookaheads):
            item.lookaheads = item.lookaheads.union(new_lookahead)

        return True

    def BuildAutomatonLR1(self):
        super().BuildAutomatonLR1()

        states = list(self.automaton)
        new_states = []
        visited = {}

        for i, state in enumerate(states):
            if state not in visited:
                # creates items
                items = [item.Center() for item in state.state]

                # check for states with same center
                for state2 in states[i:]:
                    if LALRParser.MergueItemsLookaheads(items, state2.state):
                        visited[state2] = len(new_states)

                # add new state
                new_states.append(State(frozenset(items), True))

        # making transitions
        for state in states:
            new_state = new_states[visited[state]]
            for symbol, transitions in state.transitions.items():
                for state2 in transitions:
                    new_state2 = new_states[visited[state2]]
                    # check if the transition already exists
                    if symbol not in new_state.transitions or new_state2 not in new_state.transitions[symbol]:
                        new_state.add_transition(symbol, new_state2)

        new_states[0].set_formatter(empty_formatter)
        self.automaton = new_states[0]

class DerivationTree:

    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def AddChild(self, child_tree):
        self.children.append(child_tree)

    def GetTreeAt(parser, index, parser_type='left'):
        production = parser[index]
        tree = DerivationTree(production.Left)
        end = index + 1

        sentence = reversed(production.Right) if parser_type == 'right' else production.Right

        for symbol in sentence:
            if symbol.IsTerminal:
                tree.AddChild(DerivationTree(symbol))
            else:
                ctree, end = DerivationTree.GetTreeAt(parser, end, parser_type)
                tree.AddChild(ctree)

        if parser_type == 'right': 
            tree.children.reverse()
        
        return tree, end

    def GetTree(parser, parser_type='left'):
        return DerivationTree.GetTreeAt(parser, 0, parser_type)[0]

    def Graph(self):
        G = pydot.Dot(rankdir='TD', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        visited = set()
        def visit(start):
            ids = id(start)
            if ids not in visited:
                visited.add(ids)
                G.add_node(pydot.Node(ids, label=start.symbol.Name, shape='circle', style='bold' if isinstance(start.symbol, Terminal) else ''))
                for tree in start.children:
                    visit(tree)
                    G.add_edge(pydot.Edge(ids, id(tree), labeldistance=2))

        visit(self)
        G.add_edge(pydot.Edge('start', id(self), label='', style='dashed'))

        return G

    def _repr_svg_(self):
        try:
            return self.Graph().create_svg().decode('utf8')
        except:
            pass

    def __str__(self):
        return self.symbol.Name + '[' + ']['.join(str(child) for child in self.childrens) + ']'

