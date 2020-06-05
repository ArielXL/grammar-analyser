from cmp.pycompiler import *
from cmp.type_check import type_check
from cmp.utils_grammar import UtilsGrammar
from cmp.utils_parsers import UtilsParsers

@type_check
def PrintFirsts(firsts : dict) -> None:
    for i in firsts:
        print(f'First({i}) =  {firsts[i]}')

@type_check
def PrintFollows(follows : dict) -> None:
    for i in follows:
        print(f'Follow({i}) = {follows[i]}')

@type_check
def TestingFirstAndFollow(G : Grammar) -> None:

    print('\nPROBANDO FIRSTS')
    firsts = UtilsParsers.ComputeFirsts(G)
    PrintFirsts(firsts)

    print('\nPROBANDO FOLLOWS')
    follows = UtilsParsers.ComputeFollows(G, firsts)
    PrintFollows(follows)