#!/usr/bin/env python3


"""N queens problem.

The (well-known) problem is due to Niklaus Wirth.

This solution is inspired by Dijkstra (Structured Programming).  It is
a classic recursive backtracking approach.
"""


N = 8                                   # Default; command line overrides


class Queens:
    """Classe queens."""

    def __init__(self, n=N):
        """Iniciacao da classe."""
        self.n = n
        self.reset()

    def reset(self):
        """Reset dos valores."""
        n = self.n                      # [RC] Numero de rainhas
        self.y = [None] * n             # Where is the queen in column x
        self.row = [0] * n              # Is row[y] safe?
        self.up = [0] * (2*n-1)         # Is upward diagonal[x-y] safe?
        self.down = [0] * (2*n-1)       # Is downward diagonal[x+y] safe?
        self.nfound = 0                 # Instrumentation

    def solve(self, x=0):               # Recursive solver
        """."""
        # print("")
        # print("")
        # print("[SOLVE -------------------------------------------------------")
        # print("[SOLVE -------------------------------------------------------")
        # print("[SOLVE x]", x)
        # print("[SOLVE self.n]", self.n)
        # print("[SOLVE self.y]", self.y)
        # print("[SOLVE self.row]", self.row)
        # print("[SOLVE self.up]", self.up)
        # print("[SOLVE self.down]", self.down)
        # print("[SOLVE self.nfound]", self.nfound)
        # print("")

        for y in range(self.n):         # [RC] Para cada rainha (coluna)
            # print("        [SOLVE ++++++++++++++++++++++++++++++++++++++ (in if)]")
            # print("        [y]", y)
            if self.safe(x, y):
                # print("        [safe(", x, ", ", y, ")]")
                self.place(x, y)
                if x+1 == self.n:
                    # print("[SOLVE] display() x=", x, ", y=", y, ")       <-----")
                    self.display()
                else:
                    self.solve(x+1)
                # print("[SOLVE] remove(", x, ", ", y, ")       <-----")
                self.remove(x, y)
            # else:
            #     print("        [NOT safe(", x, ", ", y, ")]")

            # print("        [self.n]", self.n)
            # print("        [self.y]", self.y)
            # print("        [self.row]", self.row)
            # print("        [self.up]", self.up)
            # print("        [self.down]", self.down)
            # print("        [self.nfound]", self.nfound)

        # print("    [SOLVE ====================================== (out if)]")
        # print("    [y]", y)
        # print("    [self.n]", self.n)
        # print("    [self.y]", self.y)
        # print("    [self.row]", self.row)
        # print("    [self.up]", self.up)
        # print("    [self.down]", self.down)
        # print("    [self.nfound]", self.nfound)

    def safe(self, x, y):
        """Verifica se a rainha esta a salvo."""
        # print("[SAFE self.row]", self.row)
        # print("[SAFE self.up]", self.up)
        # print("[SAFE self.down]", self.down)
        # print("[SAFE] self.row[", y, "]=", self.row[y],
        #      " > self.up[", x, "-", y, "]=", self.up[x-y],
        #      " > self.down[", x, "+", y, "]=", self.down[x+y])
        result = not self.row[y] and not self.up[x-y] and not self.down[x+y]
        # print("[SAFE] RETURN", result)
        return result

    def place(self, x, y):
        """Coloca a rainha."""
        # print("[place] x=", x, " y=", y)
        self.y[x] = y
        self.row[y] = 1
        self.up[x-y] = 1
        self.down[x+y] = 1

    def remove(self, x, y):
        """."""
        # print("[remove] x=", x, " y=", y)
        self.y[x] = None
        self.row[y] = 0
        self.up[x-y] = 0
        self.down[x+y] = 0

    silent = 0                          # If true, count solutions only

    def display(self):
        """."""
        self.nfound = self.nfound + 1
        if self.silent:
            return
        print('+-' + '--'*self.n + '+')
        for y in range(self.n-1, -1, -1):
            print('|', end=' ')
            for x in range(self.n):
                if self.y[x] == y:
                    print("Q", end=' ')
                else:
                    print(".", end=' ')
            print('|')
        print('+-' + '--'*self.n + '+')

        # print("    [DISPLAY ###################################### BEGIN]")
        # print("    [self.n]", self.n)
        # print("    [self.y]", self.y)
        # print("    [self.row]", self.row)
        # print("    [self.up]", self.up)
        # print("    [self.down]", self.down)
        # print("    [self.nfound]", self.nfound)
        # print("    [DISPLAY ###################################### END]")
        # print("")


def main():
    """."""
    import sys
    import os

    silent = 0
    n = N

    os.system('cls')

    if sys.argv[1:2] == ['-n']:
        silent = 1
        del sys.argv[1]

    if sys.argv[1:]:
        n = int(sys.argv[1])

    q = Queens(n)
    q.silent = silent
    q.solve()
    print("Found", q.nfound, "solutions.")


if __name__ == "__main__":
    main()
