import cmp.parsers
from cmp.parsers import LALRParser
from cmp.pycompiler import Grammar
from cmp.type_check import type_check
from cmp.utils_parsers import UtilsParsers

class ParserLALR:

    @type_check
    def __init__(self, G : Grammar, words : list) -> None:
        self.G = G
        self.words = words
        self.parser_lalr = LALRParser(self.G)
        self.TestingParserLALR()

    @type_check
    def TestingParserLALR(self) -> None:

        print('\nPROBANDO PARSER LALR')

        print('\nGRAMATICA AUMENTADA')
        print(self.parser_lalr.augmentedG)

        print('\nITEMS LALR')
        print(self.parser_lalr.automaton)

        # print('\nAUTOMATA LALR')
        # print(self.parser_lalr.automaton._repr_svg_())

        print('\nACTION LALR')
        print(self.parser_lalr.action)

        print('\nGOTO LR(1)')
        print(self.parser_lalr.goto)

        if self.parser_lalr.is_lr1:
            print('\nLA GRAMATICA ES LALR')
            self.Derivations(self.parser_lalr)
        else:
            print('\nLA GRAMATICA NO ES LALR')

    @type_check
    def Derivations(self, parser : cmp.parsers.LALRParser) -> None:
        
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

