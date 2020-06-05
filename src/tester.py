from cmp.utils_grammar import UtilsGrammar
from testing.grammar import TestingGrammar
from testing.first_and_follow import TestingFirstAndFollow
from testing.parser_top_down import TestingParserTopDown
from testing.parsers_bottom_up import TestingParserBottomUp

def help():
    
    print('La gramática debe ser libre del contexto y se escribe en el siguiente formato:')
    print('S -> a S b | epsilon')
    print('1. Usa -> para indicar una producción, y | para indicar múltiples producciones con la misma cabecera.')
    print('2. Usa epsilon para indicar el símbolo terminal especial de la gramática.')
    print('3. Usa \n para separar las producciones.')
    print('4. Todos los símbolos que sean cabecera de alguna producción serán los no-terminales, el resto seran considerados como terminales.')
    print('5. Use de ser posible, letras mayúsculas en la definición de los no-terminales y letras minúsculas para los terminales.')
    print('6. Entre dos símbolos contiguos deje siempre al menos un espacio.')
    print('7. Las palabras deben ser no-terminales separados por espacios.')

def main():

    help()

    print('\nENTRE LA GRAMATICA A ANALIZAR')
    grammar = input()
    # print(grammar)

    print('\nENTRE LA CANTIDAD DE CADENAS A ANALIZAR')
    words = []
    count_word = int(input())
    for i in range(count_word):
        print('ENTRE UNA CADENA')
        word = input()
        words.append(word)
    # print(words)

    TestingGrammar(grammar)
    TestingFirstAndFollow(UtilsGrammar.GetGrammar(grammar))
    TestingParserTopDown(grammar, words)
    TestingParserBottomUp(grammar, words)

if __name__ == '__main__':
    main()