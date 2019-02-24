
"""
Web scrapping tutorial...
Intended to obtain information from web pages through web scrapping...
"""


class HolyScrap:
    """Classe HolyScrap."""


    def __init__(self):
        """Iniciação da instancia da classe."""
        print("[___init___]")


    def display(self):
        """."""
        print("[DISPLAY]")


def main():
    """."""
    import sys
    import os

    os.system('cls')  # Clears the screen/terminal/console... whatever

    # Analyze the input arguments
    if sys.argv[1:2] == ['-n']:
        silent = 1
        del sys.argv[1]

    if sys.argv[1:]:
        n = int(sys.argv[1])

    hs = HolyScrap()
    hs.display()
    print("Holy scrap...")


if __name__ == "__main__":
    main()
