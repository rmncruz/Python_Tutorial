"""Primeiro programa em python."""


# ---------------------------------------------------------------------
# The built-in function dir() is used to find out which names a module defines
#
# Usage: dir(HelloWorld)

# ---------------------------------------------------------------------
# print("Hello World")

import os

# Multiline DOCSTRING
"""Tutorial python
Codigo diverso."""


# ---------------------------------------------------------------------
# Importar e Reimportar o modulo
# ---------------------------------------------------------------------
#
# import HelloWorld
#
# -----
#
# import importlib
# importlib.reload(HelloWorld)
#
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Comando para "limpar" a consola do interpretador de Python...
#
# Usage: "HelloWorld.clear()"
# or
# Usage: clear = HelloWorld.cl  ear
#        clear()
# ---------------------------------------------------------------------


def clear():
    """."""
    # clear = lambda: os.system('cls')
    os.system('clear')


# ---------------------------------------------------------------------
# x = int(input("please enter an integer: "))
#
# if x < 0:
#    x = 0
#    print("Negative changed to zero")
# elif x == 0:
#    print("Zero")
# elif x == 1:
#    print("Single")
# else:
#    print("More please...")
#
# print("")
#
#
# ---------------------------------------------------------------------
# Measure some strings:
# words = ['cat', 'window', 'defenestrate']
# for w in words:
#    print(w, len(w))
#
# print("")
#
#
# ---------------------------------------------------------------------
# for w in words[:]:  # Loop over a slice copy of the entire list.
#    if len(w) > 6:
#        words.insert(0, w)
#
# print(words)
#
# print("")
#
#
# ---------------------------------------------------------------------
# words = ['cat', 'window', 'defenestrate']
# counter = 0
# for w in words[:]:  # Loop over a slice copy of the entire list.
#    if counter > 0:
#        words.insert(0, w)
#    counter += 1
#
# print(words)
#
# print("")
#
#
# ---------------------------------------------------------------------
# Range...
# ---------------------------------------------------------------------
# for i in range(5):
#    print(i)
#
# print("")
#
#
# ---------------------------------------------------------------------
# for i in range(5, 10):
#    print(i)
#
# print("")
#
#
# ---------------------------------------------------------------------
# for i in range(0, 10, 3):
#    print(i)
#
# print("")
#
#
#  ---------------------------------------------------------------------
# for i in range(-10, -100, -30):
#    print(i)
#
# print("")
#
#
#  ---------------------------------------------------------------------
# a = ['as', 'armas', 'e', 'os', 'baroes', 'assinalados']
# for i in range(len(a)):
#    print(i, a[i])
#
# print("")
#
#
#  ---------------------------------------------------------------------
# for n in range(2, 10):
#    for x in range(2, n):
#        if n % x == 0:
#            print(n, 'equals', x, '*', n//x)
#            break
#        else:
#            # loop fell through without finding a factor
#            print(n, 'is a prime number')
#
# print("")


# Serie de Fibonacci ate ao numero N (indicado no WHILE)
# ---------------------------------------------------------------------
def fib1(n):
    """Fibonacci #1."""
    a, b = 0, 1

    while a < n:
        print("->", a)
        a, b = b, a + b
# def - End


# Serie de Fibonacci ate ao numero N (indicado no WHILE)
# ---------------------------------------------------------------------
def fib2(n):
    """Fibonacci #2."""
    a, b = 0, 1
    ctr = 1
    res = []

    while ctr <= n:
        # print("#> (", ctr, ") ", a)
        res.append(a)
        ctr, a, b = ctr + 1, b, a + b
    # while

    return res
# def - End


# ---------------------------------------------------------------------
def primeNumber(max_it):
    """Prime Numbers."""
    clear()
    # Flag que indica se o numero iterado e primo ou nao
    prime = False

    # Iniciar com os primos ate ao numero 11 (inclusive)
    # Temos assim 6 primos (1,2,3,5,7,11) carregados logo no inicio
    counter = 6
    prime_numbers = [1, 2, 3, 5, 7, 11]

    # Comecamos no 13 porque os anteriores ja estao contemplados
    # "max_it + 1", porque o range vai ate "-1" do max_it
    for n in range(13, max_it + 1, 2):
        # Iniciar a flag "prime" a True
        prime = True

        if (n-1) % 10000 == 0:
            print("=>", n, "-", counter)
        # if - End

        # Verificar se o numero na iteracao e primo ou nao
        # Caso seja divisivel por qualquer um dos indicados, nao e primo
        if n % 3 != 0 and n % 5 != 0 and n % 7 != 0 and n % 11 != 0:
            for x in range(13, n//2, 2):
                # print("=>", "n", n, "x", x, "n//2", n//2)

                # Caso o numero da iteracao seja divisivel por outro...
                if n % x == 0 and prime:
                    # Marca o numero como nao primo
                    prime = False
                    break
                # if - End
            # for - End
        else:
            prime = False
        # if - End

        if prime:
            # Caso o resultado da iteracao anterior True, entao numero primo
            prime_numbers.append(n)
            counter += 1
#            print(n, 'IS prime number')
#        else:
#            print(n, 'IS NOT prime number')
        # if - End
    # for - End

    print("There are", counter, "prime numbers")

#    return counter
    return prime_numbers
# def - End


# ---------------------------------------------------------------------
def firstNPrimeNumbers(nprimes):
    """Prime Numbers."""
    clear()
    # Flag que indica se o numero iterado e primo ou nao
    prime = False

    # Iniciar com os primos ate ao numero 11 (inclusive)
    # Temos assim 6 primos (1,2,3,5,7,11) carregados logo no inicio
    counter = 0
    prime_numbers = []     # [1, 2, 3, 5, 7, 11]

    if nprimes <= 0:
        counter = 0
        prime_numbers = []
    elif nprimes == 1:
        counter = 1
        prime_numbers = [1]
    elif nprimes == 2:
        counter = 2
        prime_numbers = [1, 2]
    elif nprimes == 3:
        counter = 3
        prime_numbers = [1, 2, 3]
    elif nprimes == 4:
        counter = 4
        prime_numbers = [1, 2, 3, 5]
    elif nprimes == 5:
        counter = 5
        prime_numbers = [1, 2, 3, 5, 7]
    elif nprimes == 6:
        counter = 6
        prime_numbers = [1, 2, 3, 5, 7, 11]
    else:
        # Comecamos no 13 porque os anteriores ja estao contemplados
        # "nprimes + 1", porque o range vai ate "-1" do nprimes
        # print("Else")
        prime_numbers = [1, 2, 3, 5, 7, 11]

        # for n in range(13, max_it + 1, 2):
        n = 11
        incremento = 2

        # Enquando o comprimento do array for menor que o numero desejado
        while len(prime_numbers) < nprimes:
            n += incremento

            # Iniciar a flag "prime" a True
            prime = True

            # if (n-1) % 10000 == 0:
            # print("=>", n, "-", counter)
            # if - End

            # Verificar se o numero na iteracao e primo ou nao
            # Caso seja divisivel por qualquer um dos seguintes, nao e primo
            if n % 3 != 0 and n % 5 != 0 and n % 7 != 0 and n % 11 != 0:
                for x in range(13, n//2, incremento):
                    # print("=>", "n", n, "x", x, "n//2", n//2)

                    # Caso o numero da iteracao seja divisivel por outro...
                    if n % x == 0 and prime:
                        # Marca o numero como nao primo
                        prime = False
                        break
                    # if - End
                # for - End
            else:
                prime = False
            # if - End

            if prime:
                # Caso o resultado da iteracao anterior seja True, entao primo
                prime_numbers.append(n)
                counter += 1
#                print(n, 'IS prime number')
#            else:
#                print(n, 'IS NOT prime number')
            # if - End

            # print("=>", n, "[", len(prime_numbers), "]")
        # while - End

        print("Returning", len(prime_numbers), "prime numbers")
    # if - End

#    return counter
    return prime_numbers
# def - End


# ---------------------------------------------------------------------
# for x in range(1, 11):
#    print(repr(x).rjust(5), repr(x*x).rjust(10),
#        repr(x*x*x).rjust(15), repr(x*x*x))


prime_numbers = firstNPrimeNumbers(15)
print(prime_numbers)
