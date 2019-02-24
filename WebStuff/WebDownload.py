
import requests
"""
Web scrapping - Web Download - tutorial...
Intended to download any file from the web...
"""


# class WebDownload:
#     """Classe WebDownload."""

#     def __init__(self):
#         """Iniciação da instancia da classe."""
#         print("[___init___]")
#         self.n = 0

#     def display(self):
#         """."""
#         print("[DISPLAY]")


def main():
    """."""
    import decimal
    # import http.client
    import os
    # import requests
    import urllib

    os.system('cls')  # Clears the terminal

    originalFileName = ""

    file_url = "http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf"
    file_url = "http://oilandgas.ky.gov/Production%20Reports%20Library/2015%20-%20Gas%20Production%20-%20Counties%20A-F.xls"

    # Split the url string by '/' character (the file name will in the last position of the array)
    fileURlSplited = file_url.split("/")

    # Get the last string within the array and converts the URL string characters to "normal" characters
    originalFileName = urllib.parse.unquote(fileURlSplited[-1]) 

    chunkSum = decimal.Decimal(0)
    displayLimit = 100000

    if originalFileName != "":
        r = requests.get(file_url, stream=True)

        # Get the file size... in several measures
        contentLength_byte = decimal.Decimal(r.headers.get("Content-Length"))
        contentLength_kilo = decimal.Decimal(contentLength_byte / 1024)
        contentLength_mega = decimal.Decimal(contentLength_kilo / 1024)
        # print("Content-Length:", contentLength_byte, "B")
        # print("Content-Length:", round(contentLength_kilo, 2), "KB")
        # print("Content-Length:", round(contentLength_mega, 2), "MB")

        with open("C:\\Users\\rui.m.da.cruz\\OneDrive - Accenture\\RCruz\\Tech\\Python\\Tutorial\\LixoWeb\\" + originalFileName, "wb") as pdf:
            for chunk in r.iter_content(chunk_size = 1024):
    
                # writing one chunk at a time to pdf file
                if chunk:
                    pdf.write(chunk)

                chunkSum += len(chunk)

                if chunkSum > displayLimit:
                    os.system("cls")  # Clears the terminal
                    print("Downloaded:", str(round(chunkSum, 0)).rjust(len(str(contentLength_byte))), "of", round(contentLength_byte, 0))
                    displayLimit += 100000

        os.system("cls")  # Clears the terminal
        print("Downloaded:", str(round(chunkSum, 0)).rjust(len(str(contentLength_byte))), "of", round(contentLength_byte, 0))

        # print("Content-Length:", contentLength_byte, "B")
        # print("Content-Length:", round(contentLength_kilo, 2), "KB")
        # print("Content-Length:", round(contentLength_mega, 2), "MB")

if __name__ == "__main__":
    main()
