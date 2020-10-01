# Analizador de Gramáticas

## Objetivos de la aplicación

Dada una gramática libre del contexto realiza los siguientes análisis:

1. Calcular su gramática equivalente pero sin recursividad izquierda inmediata ni prefijos comunes ni producciones innecesarias.
2. Calcular los conjuntos *first* y *follow*.
3. Determinar si la gramática es *LL(1)*.
4. Realizar un análisis con los parsers *SLR*, *LR* y *LALR*.
5. Por cada tipo de parser muestre la tabla del método predictivo no recursivo y los árboles de derivación para un conjunto de cadenas provistas.
6. En caso de que la gramática sea regular, imprimir el autómata regular y la expresión regular equivalente a la gramática.

Para un mejor entendimiento de los objetivos anteriores lea el documento [`Notas de Conferencia`](/docs/Libro.pdf).

## Ejecutando la aplicación

Para lanzar la aplicación de escritorio, ejecute las siguientes instrucciones:

```bash
$ cd src
$ make run
```

## Sobre la implementación

Esta aplicación puede ser ejecutada en los sistemas operativos *window* y *linux*, siempre y cuando esté instalado *python3* y *PyQt5*.

## Sobre los autores

Est. Liset Silva Oropesa l.silva@estudiantes.matcom.uh.cu

Est. Ariel Plasencia Díaz a.plasencia@estudiantes.matcom.uh.cu
