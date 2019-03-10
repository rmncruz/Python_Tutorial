
import decimal
import datetime
import os
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# EUROPA
# https://www.pordata.pt/Europa/Quadro+Resumo/Alemanha-230971
# https://www.pordata.pt/Europa/Quadro+Resumo/%C3%81ustria-230972
# https://www.pordata.pt/Europa/Quadro+Resumo/B%C3%A9lgica-230973
# https://www.pordata.pt/Europa/Quadro+Resumo/Bulg%C3%A1ria-230974
# https://www.pordata.pt/Europa/Quadro+Resumo/Chipre-230975
# https://www.pordata.pt/Europa/Quadro+Resumo/Cro%C3%A1cia-231012
# https://www.pordata.pt/Europa/Quadro+Resumo/Dinamarca-230976
# https://www.pordata.pt/Europa/Quadro+Resumo/Eslov%C3%A1quia-230977
# https://www.pordata.pt/Europa/Quadro+Resumo/Eslov%C3%A9nia-230978
# https://www.pordata.pt/Europa/Quadro+Resumo/Espanha-230979
# https://www.pordata.pt/Europa/Quadro+Resumo/Est%C3%B3nia-230981
# https://www.pordata.pt/Europa/Quadro+Resumo/Finl%C3%A2ndia-230982
# https://www.pordata.pt/Europa/Quadro+Resumo/Fran%C3%A7a-230983
# https://www.pordata.pt/Europa/Quadro+Resumo/Gr%C3%A9cia-230984
# https://www.pordata.pt/Europa/Quadro+Resumo/Hungria-230985
# https://www.pordata.pt/Europa/Quadro+Resumo/It%C3%A1lia-230988
# https://www.pordata.pt/Europa/Quadro+Resumo/Irlanda-230986
# https://www.pordata.pt/Europa/Quadro+Resumo/Litu%C3%A2nia-230991
# https://www.pordata.pt/Europa/Quadro+Resumo/Let%C3%B3nia-230990
# https://www.pordata.pt/Europa/Quadro+Resumo/Luxemburgo-230992
# https://www.pordata.pt/Europa/Quadro+Resumo/Malta-230993
# https://www.pordata.pt/Europa/Quadro+Resumo/Pa%C3%ADses+Baixos-230996
# https://www.pordata.pt/Europa/Quadro+Resumo/Pol%C3%B3nia-230997
# https://www.pordata.pt/Europa/Quadro+Resumo/Portugal-230998
# https://www.pordata.pt/Europa/Quadro+Resumo/Reino+Unido-230999
# https://www.pordata.pt/Europa/Quadro+Resumo/Rep%C3%BAblica+Checa-231000
# https://www.pordata.pt/Europa/Quadro+Resumo/Rom%C3%A9nia-231001
# https://www.pordata.pt/Europa/Quadro+Resumo/Su%C3%A9cia-231002


# 1. Get site content
# 2. Get raw data content
# 3. Transform data content
# 4. Store data

class PORDATAEuropa(object):

    # Class initialization
    def __init__(self, p_url):
        """Class initialization."""
        self.reset(p_url)



    # Class variables/objects reset
    def reset(self, p_url):
        """Class variables/objects reset."""
        self.url = p_url
        self.mtrx_anos = []
        self.mtrx_paises = []
        self.mtrx_dados = []



    # Create web response object
    def get_raw_site_content(self):
        """create web response object."""
        v_raw_site_content = requests.get(self.url)

        return v_raw_site_content



    # 
    def get_data_content(self, p_site_content, p_html_element, p_element_tag, p_element_tag_value):
        """."""
        # create beautiful-soup object
        v_soup = BeautifulSoup(p_site_content.content, 'html5lib')

	    # find all links on web-page
        # v_table = soup.find( "table", { "id" : "QrTable" })
        # If no "p_element_tag" and no "p_element_tag_value" (both not empty)
        if not p_element_tag and not p_element_tag_value:
            v_table = v_soup.findAll( p_html_element )
        else:
            v_table = v_soup.find( p_html_element, { p_element_tag : p_element_tag_value })
        
        return v_table



    # 
    def get_data_attribute(self, p_data_content, p_element_attr):
        """."""
        v_data_attribute = p_data_content.attrs[p_element_attr]
        
        return v_data_attribute



    # 
    def transform_table_header_content(self, p_data_content):
        """."""
        v_thead = None
        v_tr = None
        v_td = None

        # Get the html "thead" code
        v_thead = p_data_content.findAll("thead")

        # Get the "thead" "tr"'s
        v_tr = v_thead[0].findAll("tr")

        # linha dos anos (v_tr[0])
        v_td = v_tr[0].findAll("td")

        for l_elem in v_td:
            if repr(l_elem.attrs["class"]).replace("[","").replace("]","").replace("'","") == "QrHeaderYear":
                self.mtrx_anos.append(l_elem.string)

        v_aux_paises = []   # array auxiliar de paises

        # linha dos paises (v_tr[0])
        v_td = v_tr[1].findAll("td")

        for l_elem in v_td:
            if repr(l_elem.attrs["class"]).replace("[","").replace("]","").replace("'","") == "QrHeaderTerritory":
                v_aux_paises.append(l_elem.string)   # adiciona o pais ao array auxiliar...

            # Grupo de paises terminou
            if repr(l_elem.attrs["class"]).replace("[","").replace("]","").replace("'","") == "QrHeaderEmptyYearSeparator":
                self.mtrx_paises.append(v_aux_paises)         # adiciona a lista auxiliar de paises a lista de paises
                v_aux_paises = []                        # reset do array auxiliar de paises

        # Quando sair da iteracao dos paises, guarda o conteudo do array auxiliar de paises
        self.mtrx_paises.append(v_aux_paises)

        return



    # 
    def transform_table_data_content(self, p_data_content):
        """."""
        v_tbody = None
        v_tr = None
        v_td = None

        # Get the html "TBODY" code
        v_tbody = p_data_content.findAll("tbody")

        # Get the list of rows "TR"
        v_tr = v_tbody[0].findAll("tr")

        v_aux_values = []

        # For each row "TR"
        for v_aux_tr in v_tr:
            # Get the list of row columns "TD"
            v_td = v_aux_tr.findAll("td")

            v_aux_values = []

            # For each column "TD"
            for v_aux_td in v_td:
                xpto = 0






        for l_elem in v_td:
            if repr(l_elem.attrs["class"]).replace("[","").replace("]","").replace("'","") == "QrHeaderYear":
                self.mtrx_anos.append(l_elem.string)

        v_aux_paises = []   # array auxiliar de paises

        # linha dos paises (v_tr[0])
        v_td = v_tr[1].findAll("td")

        for l_elem in v_td:
            if repr(l_elem.attrs["class"]).replace("[","").replace("]","").replace("'","") == "QrHeaderTerritory":
                v_aux_paises.append(l_elem.string)   # adiciona o pais ao array auxiliar...

            # Grupo de paises terminou
            if repr(l_elem.attrs["class"]).replace("[","").replace("]","").replace("'","") == "QrHeaderEmptyYearSeparator":
                self.mtrx_paises.append(v_aux_paises)         # adiciona a lista auxiliar de paises a lista de paises
                v_aux_paises = []                        # reset do array auxiliar de paises

        # Quando sair da iteracao dos paises, guarda o conteudo do array auxiliar de paises
        self.mtrx_paises.append(v_aux_paises)


        return


    def store_data_content(self, p_data_content):
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



# Obtains the video links within the url provided
def get_web_links(p_archive_url, p_link_extension):
	""" Obtains the video links within the url provided """
	# create response object
	v_r = requests.get(p_archive_url)

	# create beautiful-soup object
	v_soup = BeautifulSoup(v_r.content, 'html5lib')

	# find all links on web-page
	v_links = v_soup.findAll('a')

	# filter the link sending with .mp4
	v_video_links = [p_archive_url + link['href']
                for link in v_links if link['href'].endswith(p_link_extension)]
                # for link in v_links if link['href'].endswith('mp4')]

	return v_video_links



# Iterate through all links in video_links and download them one by one
def download_video_series(video_links):
	"""iterate through all links in video_links and download them one by one"""

	for link in video_links:
		download_video(link)

	print("All videos downloaded!")
	return



# Downloads the indicated video
def download_video(p_link):
	""" Downloads the indicated video """

	# obtain filename by splitting url and getting
	# last string
	v_file_name = p_link.split('/')[-1]

	# print("Downloading file:", file_name)


	# create response object
	v_r = requests.get(p_link, stream=True)

	# File "content" length
	v_content_length_byte = decimal.Decimal(v_r.headers.get("Content-Length"))

	# Sum the downloaded content length
	v_chunk_sum = decimal.Decimal(0)
	# Quantity to control the download information display
	v_display_limit = 250000
	# Download start time
	v_start_time = datetime.datetime.now()

	# download started
	# with open( v_file_name, 'wb') as f:
	for chunk in v_r.iter_content(chunk_size=1024*1024):
			#if chunk:
			#    f.write(chunk)

		v_chunk_sum += len(chunk)

		if v_chunk_sum > v_display_limit:
			os.system("cls")  # Clears the terminal
			display_download_info(v_file_name, v_content_length_byte, v_chunk_sum, v_start_time)
			v_display_limit += 100000

	print(v_file_name, "downloaded!")
	return



# Removes the duplicated values from the provided list.
# The output list values order might not be the same as the provided list values order
def remove_duplicated_values(p_originav_list):
    """ Removes the duplicated values from the provided list.
	    The output list values order might not be the same as the provided list values order """

    v_list_without_duplicated_values = list(set(p_originav_list))
    return v_list_without_duplicated_values



# Prints the download related information
def display_download_info(p_file_name, p_content_length, p_chunk_sum, p_start_time):
    """ Prints the download related information """

	# Download percentage
    v_downv_percent = decimal.Decimal((p_chunk_sum / p_content_length) * 100)
	# Current time
    v_current_time = datetime.datetime.now()
    # Time difference in seconds
    v_time_diff_seconds = decimal.Decimal((v_current_time - p_start_time).seconds)
	# Download speed in KB/s
    v_downv_speed = decimal.Decimal((p_chunk_sum / v_time_diff_seconds) / 1024)

	# print("Downloaded:", str(round(chunkSum, 0)).rjust(
	# len(str(contentLength_byte))), "of", round(contentLength_byte, 0))

    print("Downloaded",
			p_file_name,
			":",
	    	str(round(v_downv_percent, 2)).rjust(6),
	    	"% (",
	    	str(round(p_chunk_sum, 0)).rjust(
	    	    len(str(p_content_length))),
	    	") of",
	    	round(p_content_length, 0),
	    	"(",
	    	round(v_downv_speed, 0),
	    	"KB/s )"
	    )
    return



# if __name__ == "__main__":
#
# 	# sys.stdout.write("Hello World!")
#
# 	# getting all video links
# 	v_video_links = get_web_links(archive_url, "mp4")
#
#     # Remove duplicated values from list
# 	v_video_links2 = remove_duplicated_values(v_video_links)
#
# 	# download all videos
# 	download_video_series(v_video_links2)



# Main method...
def main():
    """."""

    os.system('cls')

    v_options = Options()
    # v_options.add_argument("--headless")   # "--headless" don't open the chrome web browser...
    
    # v_driver = webdriver.Firefox(executable_path="/Users/rcruz/Development/Tools/PythonTools/geckodriver")
    v_driver = webdriver.Chrome(executable_path="/Users/rcruz/Development/Tools/PythonTools/chromedriver", options=v_options)

    # Give time for iframe to load...
    v_driver.implicitly_wait(30)
    # time.sleep(3)    

    # v_driver.maximize_window()

    v_driver.get("https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_indicadores&contecto=pi&indOcorrCod=0008235&selTab=tab0&xlang=pt")

#    wait(v_driver, 10).until(EC.frame_to_be_available_and_switch_to_it(v_driver.find_element_by_xpath("//iframe")))

    # Switch to the iframe
#    v_driver.switch_to.frame(v_driver.find_element_by_tag_name("iframe"))

    # Get list of iframes present on the web page
    v_iframes = v_driver.find_elements_by_tag_name("iframe")

    # Flag to identify if the desired "iframe" was found or not
    v_found = False

    for l_iframe in v_iframes:
        v_driver.switch_to_frame(l_iframe)
        # If id "frmIndicador" exists then we are at the desired iframe
        try:
            l_form = v_driver.find_element_by_id("frmIndicador")
            if l_form:
                print("Encontramos o IFRAME!!!")
                v_found = True
                v_bs_content = BeautifulSoup(v_driver.page_source, "html5lib") # "lxml")
        except:
            pass
        v_driver.switch_to_default_content()











    # RC 20190304 p = PORDATAEuropa("https://www.pordata.pt/Europa/Quadro+Resumo/Alemanha-230971")
    p = PORDATAEuropa("https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_indicadores&contecto=pi&indOcorrCod=0008235&selTab=tab0&xlang=pt")


    v_raw_site_content = p.get_raw_site_content()

    # RC 20190304 v_data_content = p.get_data_content(v_raw_site_content, "table", "id", "QrTable")
    # Get the "IFRAME" object...
    v_data_content = p.get_data_content(v_raw_site_content, "iframe", None, None)

    # Get the "IFRAME" source...
    v_iframe_element = p.get_data_attribute(v_data_content[0], "src")

    # v_iframe_response = urllib3.urlopen(v_iframe_element)
    # iframe_soup = BeautifulSoup(v_iframe_response)

    p.transform_table_header_content(v_data_content)

    p.transform_table_data_content(v_data_content)

    print("*****  THE END  *****")



if __name__ == "__main__":
    main()
