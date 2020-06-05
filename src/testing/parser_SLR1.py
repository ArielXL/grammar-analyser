from cmp.parsers import SLR1Parser
from cmp.pycompiler import Grammar
from cmp.type_check import type_check
from cmp.utils_parsers import UtilsParsers

class ParserSLR1:

    @type_check
    def __init__(self, G : Grammar, words : list) -> None:
        self.G = G
        self.words = words
        self.parser_slr1 = SLR1Parser(self.G)
        self.TestingParserSLR1()

    @type_check
    def TestingParserSLR1(self) -> None:

        print('\nPROBANDO PARSER SLR(1)')

        print('\nGRAMATICA AUMENTADA')
        print(self.parser_slr1.augmentedG)

        print('\nITEMS SLR(1)')
        print(self.parser_slr1.automaton)

        # print('\nAUTOMATA SLR(1)')
        # print(self.parser_slr1.automaton._repr_svg_())

        print('\nACTION SLR(1)')
        print(self.parser_slr1.action)

        print('\nGOTO SLR(1)')
        print(self.parser_slr1.goto)

        if self.parser_slr1.is_slr1:
            print('\nLA GRAMATICA ES SLR(1)')
            self.Derivations(self.parser_slr1)
        else:
            print('\nLA GRAMATICA NO ES SLR(1)')

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

