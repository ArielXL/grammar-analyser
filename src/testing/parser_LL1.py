from sys import stdout
from cmp.parsers import LL1Parser
from cmp.pycompiler import Grammar
from cmp.type_check import type_check
from cmp.utils_parsers import UtilsParsers

class ParserLL1:

    @type_check
    def __init__(self, G : Grammar, words : list) -> None:
        self.G = G
        self.words = words
        self.firsts = UtilsParsers.ComputeFirsts(self.G)
        self.follows = UtilsParsers.ComputeFollows(self.G, self.firsts)
        self.TestingParserLL1()

    @type_check
    def TestingParserLL1(self) -> None:

        print('\nPROBANDO PARSER LL(1)')

        self.ll1_table, is_ll1 = LL1Parser.Build_LL1_Table(self.G, self.firsts, self.follows)
        parser_ll1 = LL1Parser.NonRecursivePredictiveMethod(self.G, self.ll1_table, self.firsts, self.follows)
        
        if is_ll1:
            print('\nLA GRAMATICA ES LL(1)')
            self.Derivations(parser_ll1)
        else:
            print('\nLA GRAMATICA NO ES LL(1)')

        table = self.BuildTable()
        self.PrintTable(table, 25)

    @type_check
    def BuildTable(self) -> list:
        
        table = [[None for j in range(len(self.G.terminals) + 2)] for i in range(len(self.G.nonTerminals) + 1)]
        table[0][0] = 'states'

        for i in range(len(self.G.terminals)):
            terminal = self.G.terminals[i]
            table[0][i + 1] = terminal
        table[0][len(self.G.terminals) + 1] = '$'

        for i in range(len(self.G.nonTerminals)):
            non_terminal = self.G.nonTerminals[i]
            table[i + 1][0] = non_terminal

        pos1, pos2 = 0, 0
        for i in self.ll1_table:
            pos1 += 1
            pos2 = 0
            for j in self.ll1_table[i]:
                pos2 += 1
                trans = self.ll1_table[i][j]
                table[pos1][pos2] = trans

        return table

    @type_check
    def PrintTable(self, table : list, spaces : int) -> None:
        print('\nTABLA LL1')
        print(self.ll1_table)
        # for i in range(len(table)):
        #     for j in range(len(table[i])):
        #         if table[i][j] == None:
        #             for _ in range(spaces):
        #                 stdout.write(' ')
        #             stdout.write('|')
        #         else:
        #             length = self.GetLength(table[i][j])
        #             dif = spaces - length
        #             mitad = int(dif / 2)

        #             for k in range(mitad):
        #                stdout.write(' ')

        #             stdout.write(str(table[i][j]))

        #             for k in range(dif - mitad):
        #                 stdout.write(' ')

        #             stdout.write('|')
        #     print()

    @type_check
    def GetLength(self, s) -> int:
        if isinstance(s, list):
            length = 0
            for i in range(len(s)):
                length += len(str(s[i]))
            return length + 4
        else:
            return len(s)

    @type_check
    def Derivations(self, parser) -> None:
        
        print('\nARBOLES DE DERIVACIONES')

        words_tokenizer = []
        for word in self.words:
            words_tokenizer.append(UtilsParsers.Tokenizer(self.G, word))

        derivations = []
        for word in words_tokenizer:
            derivations.append(parser(word))
        
        for i in range(len(derivations)):
            if derivations[i] is None:
                print(f'LA CADENA {self.words[i]} NO PERTENECE A LA GRAMATICA')
            else:
                print(f'LA CADENA {self.words[i]} PERTENECE A LA GRAMATICA')                
                print(derivations[i])

