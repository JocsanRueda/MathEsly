import random

"""
Este script importa el módulo random.

Ejemplo de ordenamiento paso a paso usando Radix Sort para el array [100, 50, 3, 7000, 10]:

1. Ordenar por el dígito menos significativo (unidades):
    [100, 7000, 10, 50, 3]
2. Ordenar por el siguiente dígito (decenas):
    [100, 7000, 3, 10, 50]
3. Ordenar por el siguiente dígito (centenas):
    [3, 10, 50, 100, 7000]
4. Ordenar por el siguiente dígito (millares):
    [3, 10, 50, 100, 7000]

Resultado final ordenado: [3, 10, 50, 100, 7000]
"""
