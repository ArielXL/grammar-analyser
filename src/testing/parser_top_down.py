from cmp.type_check import type_check
from testing.parser_LL1 import ParserLL1
from cmp.utils_grammar import UtilsGrammar

@type_check
def TestingParserTopDown(grammar : str, words : list) -> None:

    print('\nPROBANDO PARSER DESCENDENTE')

    G = UtilsGrammar.GetGrammar(grammar)
    print('\nGRAMATICA')
    print(G)

    ParserLL1(G, words)
