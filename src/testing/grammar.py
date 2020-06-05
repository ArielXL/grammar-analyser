import cmp.automata
from cmp.utils import *
from cmp.type_check import type_check
from cmp.utils_grammar import UtilsGrammar

@type_check
def PrintAutomaton(regular_automaton : cmp.automata.State) -> None:

    states = list(regular_automaton)
    print(f'Estados = {states}')

    print(f'Estado inicial = {regular_automaton.state}')

    finals = []
    for state in states:
        if state.final:
            finals.append(state)
    print(f'Estados finales = {finals}')

    trans = []
    for state in states:
        for transition in state.transitions.items():
            trans.append(f'{state} -> {transition}')

    print('Transiciones')
    print(trans)

@type_check
def TestingGrammar(grammar : str) -> None:

    print('\nPROBANDO GRAMATICA')

    G = UtilsGrammar.GetGrammar(grammar)
    print('\nGRAMATICA ORIGINAL')
    print(G)

    grammar_cloned = UtilsGrammar.CloneGrammar(G)
    print('\nGRAMATICA CLONADA')
    print(grammar_cloned)

    is_not_null, acepted_symbols = UtilsGrammar.IsNotNull(grammar_cloned)

    UtilsGrammar.RemoveUnnecessaryProductions(grammar_cloned, keep_symbols = acepted_symbols)
    print('\nGRAMATICA SIN PRODUCCIONES INNECESARIAS')
    print(grammar_cloned)
    
    UtilsGrammar.RemoveLeftRecursion(grammar_cloned)
    print('\nGRAMATICA SIN RECURSION IZQUIERDA INMEDIATA')
    print(grammar_cloned)

    UtilsGrammar.RemoveCommonPrefix(grammar_cloned)
    print('\nGRAMATICA SIN PREFIJOS COMUNES')
    print(grammar_cloned)

    regular_automaton, is_regular = UtilsGrammar.BuildAutomaton(G)
    if is_regular:
        print('\nLA GRAMATICA ES REGULAR')
        print('Automata')
        PrintAutomaton(regular_automaton)
        regular_expresion = UtilsGrammar.GetRegularExpression(regular_automaton)
        print(f'Expresion regular = {regular_expresion}')
    else:
        print('\nLA GRAMATICA NO ES REGULAR')