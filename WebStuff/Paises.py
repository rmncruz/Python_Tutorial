
import decimal
import datetime
import os
import requests
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict




# EUROPA
# /Europa/Quadro+Resumo/Alemanha-230971
# /Europa/Quadro+Resumo/%C3%81ustria-230972
# /Europa/Quadro+Resumo/B%C3%A9lgica-230973
# /Europa/Quadro+Resumo/Bulg%C3%A1ria-230974
# /Europa/Quadro+Resumo/Chipre-230975
# /Europa/Quadro+Resumo/Cro%C3%A1cia-231012
# /Europa/Quadro+Resumo/Dinamarca-230976
# /Europa/Quadro+Resumo/Eslov%C3%A1quia-230977
# /Europa/Quadro+Resumo/Eslov%C3%A9nia-230978
# /Europa/Quadro+Resumo/Espanha-230979
# /Europa/Quadro+Resumo/Est%C3%B3nia-230981
# /Europa/Quadro+Resumo/Finl%C3%A2ndia-230982
# /Europa/Quadro+Resumo/Fran%C3%A7a-230983
# /Europa/Quadro+Resumo/Gr%C3%A9cia-230984
# /Europa/Quadro+Resumo/Hungria-230985
# /Europa/Quadro+Resumo/Irlanda-230986
# /Europa/Quadro+Resumo/It%C3%A1lia-230988
# /Europa/Quadro+Resumo/Let%C3%B3nia-230990
# /Europa/Quadro+Resumo/Litu%C3%A2nia-230991
# /Europa/Quadro+Resumo/Luxemburgo-230992
# /Europa/Quadro+Resumo/Malta-230993
# /Europa/Quadro+Resumo/Pa%C3%ADses+Baixos-230996
# /Europa/Quadro+Resumo/Pol%C3%B3nia-230997
# /Europa/Quadro+Resumo/Portugal-230998
# /Europa/Quadro+Resumo/Reino+Unido-230999
# /Europa/Quadro+Resumo/Rep%C3%BAblica+Checa-231000
# /Europa/Quadro+Resumo/Rom%C3%A9nia-231001
# /Europa/Quadro+Resumo/Su%C3%A9cia-231002


# 1. Get site content
# 2. Get raw data content
# 3. Transform data content
# 4. Store data

class Paises(object):


    mtrx_anos = []
    mtrx_paises = []


    def __init__(self, p_url):
        """Iniciação da classe."""
        self.url = p_url
        self.reset()


    def reset(self, p_url):
        """Reset dos valores."""
        self.url = p_url
        self.mtrx_anos = []
        self.mtrx_paises = []


    def reset(self):
        """Reset dos valores."""
        self.mtrx_anos = []
        self.mtrx_paises = []


    def get_raw_site_content(self):
        """create response object"""
        l_raw_site_content = requests.get(self.url)

        return l_raw_site_content


    def get_data_content(self, p_site_content, p_html_element, p_element_tag, p_element_tag_value):
        """."""
        # create beautiful-soup object
        l_soup = BeautifulSoup(p_site_content.content, 'html5lib')

	    # find all links on web-page
        # l_table = soup.find( "table", { "id" : "QrTable" })
        # If no "p_element_tag" and no "p_element_tag_value" (both not empty)
        if not p_element_tag and not p_element_tag_value:
            l_table = l_soup.findAll( p_html_element )
        else:
            l_table = l_soup.find( p_html_element, { p_element_tag : p_element_tag_value })
        
        return l_table


    def transform_table_header_content(self, p_data_content):
        """."""
        l_thead = None
        l_tr = None
        l_td = None

        # Get the html "thead" code
        l_thead = p_data_content.findAll("thead")

        # Get the "thead" "tr"'s
        l_tr = l_thead[0].findAll("tr")

        # linha dos anos (l_tr[0])
        l_td = l_tr[0].findAll("td")

        for l_elem in l_td:
            if repr(l_elem.attrs['class']).replace("[","").replace("]","").replace("'","") == "QrHeaderYear":
                self.mtrx_anos.append(l_elem.string)

        l_aux_paises = []   # array auxiliar de paises

        # linha dos paises (l_tr[0])
        l_td = l_tr[1].findAll("td")

        for l_elem in l_td:
            if repr(l_elem.attrs['class']).replace("[","").replace("]","").replace("'","") == "QrHeaderTerritory":
                l_aux_paises.append(l_elem.string)   # adiciona o pais ao array auxiliar...

            # Grupo de paises terminou
            if repr(l_elem.attrs['class']).replace("[","").replace("]","").replace("'","") == "QrHeaderEmptyYearSeparator":
                self.mtrx_paises.append(l_aux_paises)         # adiciona a lista auxiliar de paises a lista de paises
                l_aux_paises = []                        # reset do array auxiliar de paises

        # Quando sair da iteracao dos paises, guarda o conteudo do array auxiliar de paises
        self.mtrx_paises.append(l_aux_paises)

        return


    def transform_table_data_content(p_data_content):
        """."""
        l_tbody = None
        l_tr = None
        l_td = None

        # Get the html "thead" code
        l_tbody = p_data_content.findAll("tbody")

        # Get the list od all "TR"sGet the "thead" "tr"'s
        l_tr = l_tbody[0].findAll("tr")

        l_aux_values = []

        for l_aux_tr in l_tr:
            # For each
            l_td = l_aux_tr.findAll("td")

            l_aux_values = []

            for l_aux_td in l_td:
                xpto = 0






        for l_elem in l_td:
            if repr(l_elem.attrs['class']).replace("[","").replace("]","").replace("'","") == "QrHeaderYear":
                self.mtrx_anos.append(l_elem.string)

        l_aux_paises = []   # array auxiliar de paises

        # linha dos paises (l_tr[0])
        l_td = l_tr[1].findAll("td")

        for l_elem in l_td:
            if repr(l_elem.attrs['class']).replace("[","").replace("]","").replace("'","") == "QrHeaderTerritory":
                l_aux_paises.append(l_elem.string)   # adiciona o pais ao array auxiliar...

            # Grupo de paises terminou
            if repr(l_elem.attrs['class']).replace("[","").replace("]","").replace("'","") == "QrHeaderEmptyYearSeparator":
                self.mtrx_paises.append(l_aux_paises)         # adiciona a lista auxiliar de paises a lista de paises
                l_aux_paises = []                        # reset do array auxiliar de paises

        # Quando sair da iteracao dos paises, guarda o conteudo do array auxiliar de paises
        self.mtrx_paises.append(l_aux_paises)


        return


    def store_data_content(p_data_content):
        """."""
        return


"""
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
"""


# specify the URL of the archive here
archive_url = "http://www-personal.umich.edu/~csev/books/py4inf/media/"


def get_web_links(p_archive_url, p_link_extension):
	""" Obtains the video links within the url provided """
	# create response object
	l_r = requests.get(p_archive_url)

	# create beautiful-soup object
	l_soup = BeautifulSoup(l_r.content, 'html5lib')

	# find all links on web-page
	l_links = l_soup.findAll('a')

	# filter the link sending with .mp4
	l_video_links = [p_archive_url + link['href']
                for link in l_links if link['href'].endswith(p_link_extension)]
                # for link in l_links if link['href'].endswith('mp4')]

	return l_video_links



def download_video_series(video_links):
	"""iterate through all links in video_links and download them one by one"""

	for link in video_links:
		download_video(link)

	print("All videos downloaded!")
	return



def download_video(p_link):
	""" Downloads the indicated video """

	# obtain filename by splitting url and getting
	# last string
	l_file_name = p_link.split('/')[-1]

	# print("Downloading file:", file_name)


	# create response object
	l_r = requests.get(p_link, stream=True)

	# File "content" length
	l_content_length_byte = decimal.Decimal(l_r.headers.get("Content-Length"))

	# Sum the downloaded content length
	l_chunk_sum = decimal.Decimal(0)
	# Quantity to control the download information display
	l_display_limit = 250000
	# Download start time
	l_start_time = datetime.datetime.now()

	# download started
	# with open( l_file_name, 'wb') as f:
	for chunk in l_r.iter_content(chunk_size=1024*1024):
			#if chunk:
			#    f.write(chunk)

		l_chunk_sum += len(chunk)

		if l_chunk_sum > l_display_limit:
			os.system("cls")  # Clears the terminal
			display_download_info(l_file_name, l_content_length_byte, l_chunk_sum, l_start_time)
			l_display_limit += 100000

	print(l_file_name, "downloaded!")
	return



def remove_duplicated_values(p_original_list):
    """ Removes the duplicated values from the provided list.
	    The output list values order might not be the same as the provided list values order """

    l_list_without_duplicated_values = list(set(p_original_list))
    return l_list_without_duplicated_values



def display_download_info(p_file_name, p_content_length, p_chunk_sum, p_start_time):
    """ Prints the download related information """

	# Download percentage
    l_downl_percent = decimal.Decimal((p_chunk_sum / p_content_length) * 100)
	# Current time
    l_current_time = datetime.datetime.now()
    # Time difference in seconds
    l_time_diff_seconds = decimal.Decimal((l_current_time - p_start_time).seconds)
	# Download speed in KB/s
    l_downl_speed = decimal.Decimal((p_chunk_sum / l_time_diff_seconds) / 1024)

	# print("Downloaded:", str(round(chunkSum, 0)).rjust(
	# len(str(contentLength_byte))), "of", round(contentLength_byte, 0))

    print("Downloaded",
			p_file_name,
			":",
	    	str(round(l_downl_percent, 2)).rjust(6),
	    	"% (",
	    	str(round(p_chunk_sum, 0)).rjust(
	    	    len(str(p_content_length))),
	    	") of",
	    	round(p_content_length, 0),
	    	"(",
	    	round(l_downl_speed, 0),
	    	"KB/s )"
	    )
    return


# if __name__ == "__main__":
#
# 	# sys.stdout.write("Hello World!")
#
# 	# getting all video links
# 	l_video_links = get_web_links(archive_url, "mp4")
#
#     # Remove duplicated values from list
# 	l_video_links2 = remove_duplicated_values(l_video_links)
#
# 	# download all videos
# 	download_video_series(l_video_links2)


def main():
    """."""

    os.system('cls')

    p = Paises("/Europa/Quadro+Resumo/Alemanha-230971")

    l_raw_site_content = p.get_raw_site_content()

    l_data_content = p.get_data_content(l_raw_site_content, "table", "id", "QrTable")

    p.transform_table_header_content(l_data_content)

    p.transform_table_data_content(l_data_content)

    print("*****  THE END  *****")



if __name__ == "__main__":
    main()
