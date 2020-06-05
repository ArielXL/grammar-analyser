from cmp.parsers import LR1Parser
from cmp.pycompiler import Grammar
from cmp.type_check import type_check
from cmp.utils_parsers import UtilsParsers

class ParserLR1:

    @type_check
    def __init__(self, G : Grammar, words : list) -> None:
        self.G = G
        self.words = words
        self.parser_lr1 = LR1Parser(self.G)
        self.TestingParserLR1()

    @type_check
    def TestingParserLR1(self) -> None:

        print('\nPROBANDO PARSER LR(1)')

        print('\nGRAMATICA AUMENTADA')
        print(self.parser_lr1.augmentedG)

        print('\nITEMS LR(1)')
        print(self.parser_lr1.automaton)

        # print('\nAUTOMATA LR(1)')
        # print(self.parser_lr1.automaton._repr_svg_())

        print('\nACTION LR(1)')
        print(self.parser_lr1.action)

        print('\nGOTO LR(1)')
        print(self.parser_lr1.goto)

        if self.parser_lr1.is_lr1:
            print('\nLA GRAMATICA ES LR(1)')
            self.Derivations(self.parser_lr1)
        else:
            print('\nLA GRAMATICA NO ES LR(1)')

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

