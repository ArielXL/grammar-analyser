import json

class Symbol(object):

    def __init__(self, name, grammar):
        self.Name = name
        self.Grammar = grammar

    def __str__(self):
        return self.Name

    def __repr__(self):
        return repr(self.Name)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(self, other)

        raise TypeError(other)

    def __or__(self, other):

        if isinstance(other, (Sentence)):
            return SentenceList(Sentence(self), other)

        raise TypeError(other)

    @property
    def IsEpsilon(self):
        return False

    def __len__(self):
        return 1

class NonTerminal(Symbol):

    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        self.productions = []

    def __imod__(self, other):

        if isinstance(other, (Sentence)):
            p = Production(self, other)
            self.Grammar.AddProduction(p)
            return self

        if isinstance(other, tuple):

            if len(other) == 2:
                other += (None,) * len(other[0])

            if isinstance(other[0], Symbol) or isinstance(other[0], Sentence):
                p = AttributeProduction(self, other[0], other[1:])
            else:
                raise Exception("")

            self.Grammar.AddProduction(p)
            return self

        if isinstance(other, Symbol):
            p = Production(self, Sentence(other))
            self.Grammar.AddProduction(p)
            return self

        if isinstance(other, SentenceList):

            for s in other:
                p = Production(self, s)
                self.Grammar.AddProduction(p)

            return self

        raise TypeError(other)

    @property
    def IsTerminal(self):
        return False

    @property
    def IsNonTerminal(self):
        return True

    @property
    def IsEpsilon(self):
        return False

class Terminal(Symbol):

    def __init__(self, name, grammar):
        super().__init__(name, grammar)

    @property
    def IsTerminal(self):
        return True

    @property
    def IsNonTerminal(self):
        return False

    @property
    def IsEpsilon(self):
        return False

class EOF(Terminal):

    def __init__(self, Grammar):
        super().__init__('$', Grammar)

class Sentence(object):

    def __init__(self, *args):
        self._symbols = tuple(x for x in args if not x.IsEpsilon)
        self.hash = hash(self._symbols)

    def __len__(self):
        return len(self._symbols)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(*(self._symbols + (other,)))

        if isinstance(other, Sentence):
            return Sentence(*(self._symbols + other._symbols))

        raise TypeError(other)

    def __or__(self, other):
        if isinstance(other, Sentence):
            return SentenceList(self, other)

        if isinstance(other, Symbol):
            return SentenceList(self, Sentence(other))

        raise TypeError(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ("%s " * len(self._symbols) % tuple(self._symbols)).strip()

    def __iter__(self):
        return iter(self._symbols)

    def __getitem__(self, index):
        return self._symbols[index]

    def __eq__(self, other):
        return self._symbols == other._symbols

    def __hash__(self):
        return self.hash

    @property
    def IsEpsilon(self):
        return False

class SentenceList(object):

    def __init__(self, *args):
        self._sentences = list(args)

    def Add(self, symbol):
        if not symbol and (symbol is None or not symbol.IsEpsilon):
            raise ValueError(symbol)

        self._sentences.append(symbol)

    def __iter__(self):
        return iter(self._sentences)

    def __or__(self, other):
        if isinstance(other, Sentence):
            self.Add(other)
            return self

        if isinstance(other, Symbol):
            return self | Sentence(other)

class Epsilon(Terminal, Sentence):

    def __init__(self, grammar):
        super().__init__('epsilon', grammar)
        self._symbols = []


    def __str__(self):
        # return "e"
        return u'\N{GREEK SMALL LETTER EPSILON}'

    def __repr__(self):
        return 'epsilon'

    def __iter__(self):
        yield from ()

    def __len__(self):
        return 0

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    def __hash__(self):
        return hash("")

    @property
    def IsEpsilon(self):
        return True

class Production(object):

    def __init__(self, nonTerminal, sentence):

        self.Left = nonTerminal
        self.Right = sentence

    # →
    def __str__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right

    def __eq__(self, other):
        return isinstance(other, Production) and self.Left == other.Left and self.Right == other.Right

    def __hash__(self):
        return hash((self.Left, self.Right))

    @property
    def IsEpsilon(self):
        return self.Right.IsEpsilon

class AttributeProduction(Production):

    def __init__(self, nonTerminal, sentence, attributes):
        if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
            sentence = Sentence(sentence)
        super(AttributeProduction, self).__init__(nonTerminal, sentence)

        self.attributes = attributes

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right

    @property
    def IsEpsilon(self):
        return self.Right.IsEpsilon

    def syntetice(self):
        pass

class Grammar():

    def __init__(self):
        self.Productions = []
        self.nonTerminals = []
        self.terminals = []
        self.startSymbol = None
        self.pType = None
        self.Epsilon = Epsilon(self)
        self.EOF = EOF(self)

        self.symbDict = { '$': self.EOF }

    def NonTerminal(self, name, startSymbol = False):

        name = name.strip()
        if not name:
            raise Exception('Empty name')

        term = NonTerminal(name,self)

        if startSymbol:

            if self.startSymbol is None:
                self.startSymbol = term
                self.nonTerminals.insert(0, term)
            else:
                raise Exception('Cannot define more than one start symbol')
        else:
            self.nonTerminals.append(term)
        self.symbDict[name] = term
        return term

    def NonTerminals(self, names):

        ans = tuple((self.NonTerminal(x) for x in names.strip().split()))
        return ans

    def AddProduction(self, production):

        if len(self.Productions) == 0:
            self.pType = type(production)

        if production not in production.Left.productions:
            production.Left.productions.append(production)
            self.Productions.append(production)

    def Terminal(self, name):

        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = Terminal(name, self)
        self.terminals.append(term)
        self.symbDict[name] = term
        return term

    def Terminals(self, names):

        ans = tuple((self.Terminal(x) for x in names.strip().split()))
        return ans

    def __str__(self):

        grammar = 'Non-Terminals = { '
        nonterminals = ' , '.join(['%s'] * len(self.nonTerminals)) + ' }\n'
        grammar += nonterminals % tuple(self.nonTerminals)

        grammar += 'Terminals = { '
        terminals = ' , '.join(['%s'] * len(self.terminals)) + ' }\n'
        grammar += terminals % tuple(self.terminals)

        grammar += 'Productions = { '
        grammar += str(self.Productions)
        grammar += ' }'

        return grammar

    def __getitem__(self, name):
        try:
            return self.symbDict[name]
        except KeyError:
            return None

    @property
    def ToJson(self):

        productions = []

        for p in self.Productions:
            head = p.Left.Name

            body = []

            for s in p.Right:
                body.append(s.Name)

            productions.append({'Head':head, 'Body':body})

        d = {'NonTerminals':[symb.Name for symb in self.nonTerminals], 'Terminals': [symb.Name for symb in self.terminals],\
         'Productions':productions}

        return json.dumps(d)

    def FromJson(data):
        data = json.loads(data)

        G = Grammar()
        dic = {'epsilon': G.Epsilon}

        for term in data['Terminals']:
            dic[term] = G.Terminal(term)

        for i, noTerm in enumerate(data['NonTerminals']):
            dic[noTerm] = G.NonTerminal(noTerm, not i)

        for p in data['Productions']:
            head = p['Head']
            dic[head] %= sum((dic[term] for term in p['Body'][1:]), dic[p['Body'][0]])

        return G

    def Copy(self):
        G = Grammar()
        G.Productions = self.Productions.copy()
        G.nonTerminals = self.nonTerminals.copy()
        G.terminals = self.terminals.copy()
        G.pType = self.pType
        G.startSymbol = self.startSymbol
        G.Epsilon = self.Epsilon
        G.EOF = self.EOF
        G.symbDict = self.symbDict.copy()

        return G

    @property
    def IsAugmentedGrammar(self):
        augmented = 0
        for left, right in self.Productions:
            if self.startSymbol == left:
                augmented += 1
        if augmented <= 1:
            return True
        else:
            return False

    def AugmentedGrammar(self, force=False):
        if not self.IsAugmentedGrammar or force:

            G = self.Copy()
            S = G.startSymbol
            G.startSymbol = None
            SS = G.NonTerminal('S\'', True)
            if G.pType is AttributeProduction:
                SS %= S + G.Epsilon, lambda x : x
            else:
                SS %= S + G.Epsilon
 
            return G
        else:
            return self.copy()

class Item:

    def __init__(self, production, pos, lookaheads=[]):
        self.production = production
        self.pos = pos
        self.lookaheads = frozenset(look for look in lookaheads)

    def __str__(self):
        s = str(self.production.Left) + " -> "
        if len(self.production.Right) > 0:
            for i,c in enumerate(self.production.Right):
                if i == self.pos:
                    s += "."
                s += str(self.production.Right[i])
            if self.pos == len(self.production.Right):
                s += "."
        else:
            s += "."
        s += ", " + str(self.lookaheads)[10:-1]
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            (self.pos == other.pos) and
            (self.production == other.production) and
            (set(self.lookaheads) == set(other.lookaheads))
        )

    def __hash__(self):
        return hash((self.production,self.pos,self.lookaheads))

    @property
    def IsReduceItem(self):
        return len(self.production.Right) == self.pos

    @property
    def NextSymbol(self):
        if self.pos < len(self.production.Right):
            return self.production.Right[self.pos]
        else:
            return None

    def NextItem(self):
        if self.pos < len(self.production.Right):
            return Item(self.production,self.pos+1,self.lookaheads)
        else:
            return None

    def Preview(self, skip=1):
        unseen = self.production.Right[self.pos+skip:]
        return [ unseen + (lookahead,) for lookahead in self.lookaheads ]

    def Center(self):
        return Item(self.production, self.pos)