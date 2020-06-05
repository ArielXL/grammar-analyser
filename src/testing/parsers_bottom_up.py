from cmp.type_check import type_check
from testing.parser_LR1 import ParserLR1
from cmp.utils_grammar import UtilsGrammar
from testing.parser_SLR1 import ParserSLR1
from testing.parser_LALR import ParserLALR

@type_check
def TestingParserBottomUp(grammar : str, words : list) -> None:

    print('\nPROBANDO PARSER ASCENDENTE')

    G = UtilsGrammar.GetGrammar(grammar)
    print('\nGRAMATICA')
    print(G)

    ParserSLR1(G, words)

    ParserLR1(G, words)

    ParserLALR(G, words)