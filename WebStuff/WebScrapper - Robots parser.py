import os
import requests
from reppy import Robots
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerProcess
import time
import datetime
import csv



# response = requests.get("http://www.debenhams.com/robots.txt")
# test = response.text
# os.system("cls")
# print(test)
# linha = test.split("\n")
# print("")
# print("")
# print("")
# print("")
# print("")
# for i in linha:
#     print(i)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
#
# CLASS MyScrapySpider ** START **
#
# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
class MyScrapySpider(scrapy.Spider):
    """
    .
    """

    # name = "my_scrapy_spider"
    # start_urls = ['http://brickset.com/sets/year-2016']



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Overrides superclass "__ini__" method.
        Invoques super... then gets the url to parse and sets it to "start_urls"
        """
        super(MyScrapySpider, self).__init__(*args, **kwargs)

        l_name = kwargs.get("name")

        l_start_url = kwargs.get("start_url")

        if not l_start_url:
            raise ValueError("No 'start_Url'")

        if not l_name:
            raise ValueError("No 'Name'")

        # dt = datetime.strptime(date, "%m-%d-%Y")
        self.name = l_name

        self.start_urls = [l_start_url]

        pass



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def parse(self, response):
        """
        .
        """


        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath(".//span[@class='text']/text()").extract_first()

            author = quote.xpath(".//small//text()").extract_first()

            yield {'quote': text, "author": author}

        # v_extract_result = scrapy.Field()
# 
        # for l_sel in response.xpath('//tr/td/a'):
# 
        #     # l_item = IkeaItem()
# 
        #     # l_item['name'] = l_sel.xpath('a/text()').extract()
        #     # l_item['link'] = l_sel.xpath('a/@href').extract()
# 
        #     v_extract_result = l_sel.xpath('//a/@href').extract()
# 
        #     # yield l_item

        pass




    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def start_requests(self):
        """
        .
        """

        for x in self.start_urls:
            xreq = scrapy.Request(x, self.parse)
            yield xreq



    # LIXO?! text_response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')


# ---------------------------------------------------------------------------------------------------
#
# CLASS MyScrapySpider ** END **
#
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------






# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
#
# CLASS MyWebScraper ** START **
#
# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
class MyWebScraper(object):
    """Class to implement a web crawler."""
    

    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # VARIABLES
    #
    # ---------------------------------------------------------------------------------------------------

    # Constant to hold the robot file name
    c_robots_file_name = "robots.txt"
    # Default crawl delay in seconds (this value will be use case not defined within the ROBOTS.TXT file)
    c_crawl_delay = 10
    # For testing purpose, sets the maximum number of scrapes to be done - When 0 does all
    c_max_scrape_counter = 2

    # "Main" Web page url to be scraped
    # The value of this variable will be:
    #      - The value of the "Host Directive" if it exists in the ROBOTS.TXT
    #      - The original url value otherwise
    v_root_url = ""
    v_root_url_domain = ""
    # "Main" Web page url provided by the user
    v_provided_url = ""
    # The crawl delay provided by the ROBOTS.TXT file (in seconds)
    # By default we set the delay to 5 seconds...
    v_crawl_delay = 10
    # The host directive provided by the ROBOTS.TXT file
    v_rb_host_directive = ""
    # (reppy.)Robot parser
    v_robots_parser = None
    # List of urls to be validated and scraped...
    v_urls_to_scrape = []
    # List of urls successfully scraped
    v_urls_scraped = []
    # List of urls whose scrape is not allowed by ROBTOS.TXT file
    v_urls_disallowed = []
    # List of urls whose domain do not match the "main" web page domain
    v_urls_out_domain = []
    # List of objects identified by the scrape
    v_result_list = []
    # List that will provide a "map" of the site
    v_map_list = []

    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # METHODS
    #
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, p_original_url):
        """
        Iniciação da classe.
        """

        self.v_provided_url = p_original_url
        self.reset()
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def reset(self, p_provided_url):
        """
        Reset dos valores.
        """

        self.v_root_url = ""
        self.v_root_url_domain = ""
        self.v_provided_url = p_provided_url
        self.v_crawl_delay = self.c_crawl_delay
        self.v_rb_host_directive = ""
        self.v_urls_to_scrape = []
        self.v_urls_scraped = []
        self.v_urls_disallowed = []
        self.v_urls_out_domain = []
        self.v_result_list = []
        self.v_map_list = []
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def get_robot_url(self):
        """
        Returns the ROBOTS.TXT url.
        Returns the concatenation of the "Main" web page url with the value of the constant C_ROBOTS.

        TODO: Instead of using directly the "Main" web page url, we must obtain its domain and
              return the concatenation of the "Main" web page url DOMAIN with the value of the constant C_ROBOTS.
              This way we can start within any web page url, and not only the site root web page.
        """

        l_sep = ""

        # If url has value...
        if self.v_provided_url:
            # If last character of url is not "/" then set separator to "/"
            if len(self.v_provided_url) > 0 and self.v_provided_url[-1] != "/":
                l_sep = "/"

            return self.v_provided_url + l_sep + self.c_robots_file_name
        else:
            return ""
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def load_robot_file(self):
        """
        Loads the ROBOTS.TXT file content.
        Uses reppy/Robot module...
        """

        try: 
            self.v_robots_parser = Robots.fetch(self.get_robot_url())

        except:
            # In case of error/exception set the parser variable to None
            self.v_robots_parser = None
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def get_robot_parser(self):
        """
        Returns the robot parser.
        """

        return self.v_robots_parser
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def get_root_url(self):
        """
        Returns the root url for the scrape process.
        If the ROBOTS.TXT file has a host directive, then we assume that value as the root url
        Otherwise, the url provided by the user is assumed.
        """

        # If root url not yet calculated...
        if not self.v_root_url:
            # If ROBOTS.TXT contains a host directive then use it, else use user provided url
            if self.v_rb_host_directive:
                self.v_root_url = self.v_rb_host_directive
            else:
                self.v_root_url = self.v_provided_url
    
            # Determines and stores the root url domain
            self.v_root_url_domain = self.get_url_domain(self.v_root_url)

        return self.v_root_url
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def exists_url_to_be_scraped(self, p_url_to_be_scraped):
        """
        Checks if the indicates url already exists in the list of url to be scraped.
        """

        if p_url_to_be_scraped in self.v_urls_to_scrape:
            return True
        else:
            return False
    # ---------------------------------------------------------------------------------------------------


    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def add_url_to_be_scraped(self, p_url_to_be_scraped):
        """
        Adds an url to the list of url to be scraped.
        """

        self.v_urls_to_scrape.append(p_url_to_be_scraped)
    # ---------------------------------------------------------------------------------------------------


    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------

    def add_url_scraped(self, p_url_scraped):
        """
        Adds an url to the list of url scraped.
        """

        self.v_urls_scraped.append(p_url_scraped)
    # ---------------------------------------------------------------------------------------------------
 


    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def add_url_not_allowed(self, p_url_not_allowed):
        """
        Adds an url to the list of url not allowed.
        (Based on the site's ROBOTS.TXT file)
        """

        self.v_urls_disallowed.append(p_url_not_allowed)
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def add_url_out_domain(self, p_url_out_domain):
        """
        Adds an url to the list of url out of domain.
        (Urls that "point" to outside sites)
        """

        self.v_urls_out_domain.append(p_url_out_domain)
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def remove_url_to_scrape(self, p_url_to_remove):
        """
        Removes an url from the list of url to be scraped.
        """

        self.v_urls_to_scrape.remove(p_url_to_remove)
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def initialize_list_url_to_scrape(self):
        """
        Initializes the url to scrape list with the root url.
        """

        self.v_urls_to_scrape = []
        self.v_urls_to_scrape.append(self.get_root_url())
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def scrape_url_list(self):
        """
        Recursive function that will scrape all urls within the url to be scraped list.
        It gets the firt url (position [0] of the list) scrapes it, removes if from the list of 
        urls to be scraped (within method scrape_url) and processes the "new" list...
        ("new" list is the list without the processed url and with additional urls identified within the
        processed url process...) 
        """

        # If the urls to scrape list don't have any element (NULL (None) list), then exit
        if not self.v_urls_to_scrape:
            return

        # Empty list (zero elements), then exit
        if len(self.v_urls_to_scrape) == 0:
            return

        # Get the first url to be scraped from the list 
        l_url = self.v_urls_to_scrape[0]

        # TESTING
        print("[", datetime.datetime.now(), "]")

        # Wait the time defined by variable "v_crawl_delay" before scrape the url
        time.sleep(self.v_crawl_delay)

        # Scrape the url
        self.scrape_url(l_url)

        # TESTING - Get time 1 in seconds
        # l_t1 = time.time()

        # TESTING - Get time 2 in seconds
        # l_t2 = time.time()

        # TESTING - Print the time difference
        # print(int(l_t2 - l_t1))

        # The scraped url has been removed from the url to scrape list by the "scrape_url" method...
        # (so the url to scrape list has one less element - the one processed in this iteraction)

        # Recursively scrape the remaining urls to scrape
        # Takes into account the maximum scraped counter
        if len(self.v_urls_scraped) < self.c_max_scrape_counter or self.c_max_scrape_counter == 0:
            self.scrape_url_list()
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def scrape_url(self, p_url):
        """
        Scrapes the url.
        First it validates the availability of the url to be scraped.
        Then scrapes the url.
        Finally removes the url from the url to be scraped list.
        """

        # Check if the indicated url is valid to be scraped, if not then exit
        if self.url_available_to_scrape(p_url):

            # Scrape the url for links
            self.scrapes_url_for_links(p_url)

            # Adds the url to the list of scraped (processed) urls
            self.add_url_scraped(p_url)

        # Remove the url from the list of urls to be scraped (processed)
        self.remove_url_to_scrape(p_url)
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def scrapes_url_for_links(self, p_url):
        """
        Scrapes the url for links.
        The url has been previously validated for the availability of the url to be scraped, so this method 
        won't check for the url availability to be scraped
        """

        l_new_url = ""
        l_new_url_counter = 0
        l_new_url_to_scrape_counter = 0

        # If no url indicated then exit
        if not p_url:
            return
        
        # Executes the http request to the url
        l_page = requests.get(p_url, verify=False)

        # "Beautify" the http response content
        l_bsoup = BeautifulSoup(l_page.content, features="lxml")

        # Get all "<a>" elements
        for l_link in (l_bsoup.findAll("a")):

            # Increases the new url counter by 1
            l_new_url_counter += 1

            # Adds the "link relation" to the "map"
            self.v_map_list.append([p_url, l_link.get("href"), datetime.datetime.now()])

            # print(l_link.get("href"))

            # Link is None (NULL) or Empty
            if l_link.get("href") == None or len(l_link.get("href")) == 0:

                l_new_url = self.get_root_url()

            # Link has some content
            # len(l_link.get("href")) > 0:
            else:
                
                # The link starts with "/"
                if l_link.get("href")[0] == "/":
                
                    # The link "href" is just "/"
                    if len(l_link.get("href")) == 1:
                        l_new_url = self.get_root_url()
                
                    # The second character within the link is not "/"
                    elif l_link.get("href")[1] != "/":
                        l_new_url = self.get_root_url() + l_link.get("href")

                    # Link starts with "//"
                    else:
                        l_new_url = "http:" + l_link.get("href")
        
                # Link does not start with "/"
                else:
                    # Link starts with "http"
                    if l_link.get("href")[0:4] == "http":

                        l_new_url = l_link.get("href")
                
                    # Link does not start with "http"
                    else:
                        l_new_url = "http://" + l_link.get("href")


            # print("-->", l_new_url)

            # The new url is only added to the url to be scraped list if it is available for scraping 
            # and if it does not already exists in the url to be scraped list
            if self.url_available_to_scrape(l_new_url) and not self.exists_url_to_be_scraped(l_new_url):
                self.add_url_to_be_scraped(l_new_url)
                l_new_url_to_scrape_counter += 1

        print("Within URL \"", p_url, "\" ,", l_new_url_counter, "links identified and processed, from which", l_new_url_to_scrape_counter, "where added to url to scrape list")


        # x_proc = CrawlerProcess({
        #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        # })
        # x_proc.crawl(MyScrapySpider)
        # x_proc.start()  # the script will block here until the crawling is finished

        # # Get the response from the url request
        # l_resp = scrapy.http.Request(p_url)
        # 

        # try:
        #     l_my_spider = MyScrapySpider(name="my_scrapy_spider",start_url=p_url)
        #     l_my_spider.start_requests()

        # except:
        #     pass
    # ---------------------------------------------------------------------------------------------------




    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def url_available_to_scrape(self, p_url):
        """
        Checks if the indicated url available for scrape process.
        
        Returns 
            - TRUE  -> if is OK for scrape process
            - FALSE -> otherwise, not OK for scrape process

        The validations executed are the following and if it falls within one of them then the url is not valid be scraped:
            - Url already scraped (exists in url scraped list)
            - Url already disallowed by ROBOTS.TXT (exists in url not allowed list)
            - Url not allowed by ROBOTS.TXT
            - Url already in the out DOMAIN list (exist in url out domain list)
            - Url domain different from the root url domain
        """
        
        # If indicated url empty, nothing to do
        if not p_url:
            return

        # If the indicated url as already been scraped, nothing to do
        if p_url in self.v_urls_scraped:
            return

        # If the indicated url as already been excluded , nothing to do
        if p_url in self.v_urls_out_domain:
            return False

        # Checks if the indicated url domain is within the root url domain
        if self.get_url_domain(p_url) != self.v_root_url_domain:
            # If domains are different then mark the indicated url as "out of domain"
            self.add_url_out_domain(p_url)
            return False

        # If the indicated url as already been disallowed by the ROBOTS.TXT, nothing to do
        if p_url in self.v_urls_disallowed:
            return

        # Checks if the indicated url is valid within the ROBOTS.TXT, if not valid returns FALSE
        if not self.get_robot_parser().allowed(p_url, "*"):
            # If indicated url not allowed by ROBOTS.TXT then mark it as "not allowed"
            self.add_url_not_allowed(p_url)
            return False

        # If there is no impemdiment then set the indicated url as valid for scrape process...
        return True
    # ---------------------------------------------------------------------------------------------------



    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    def get_url_domain(self, p_url):
        """
        Returns the url domain.
        """

        # If indicated url is nothing...
        if not p_url:
           return None

        # Splits the url by "/"
        l_aux = p_url.split("/")   

        # If the first sting [0] starts with "HTTP", then return the thrid [2] element of the list
        if len(l_aux) >= 3 and len(l_aux[0]) >= 4 and l_aux[0][0:4].upper() == "HTTP":
            return l_aux[2]

        # Otherwise returns the first element of the list
        return l_aux[0]
    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    # def exists(p_elem, p_collection: iter):
    #     return p_elem in p_collection
    # ---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------
#
# CLASS MyWebScraper ** END **
#
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
















    # ---------------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------








    def reset(self):
        """Reset dos valores."""
        #self.mtrx_anos = []
        #self.mtrx_paises = []


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
[MAIN]
     1. Get Robots.txt from web_site_url
     2. Get crawl_delay from Robots.txt
     3. Get host_directive from Robots.txt
     4. Get list_sitemap_urls from Robots.txt
     5. If host_directive then append host_directive to urls_list_to_scrape[]
        Else append web_site_url to urls_list_to_scrape[]
     6. Append list_sitemap_urls to urls_list_to_scrape[]
     7. urls_list_disallowed[]
     8. urls_list_scraped[]
     9. urls_list_outside_domain[]
    10. [scrape_url_list()]
    11. Export urls_list_scraped[] to excel... oracle db... sqlserver db...
    12. Exit


[DEF scrape_url_list()]
     1. If len(urls_list_to_scrape[]) = 0 then exit
     2. url_to_scrape = urls_list_to_scrape[0]
     3. If url_to_scrape in urls_list_disallowed[] or urls_list_scraped[] then 
            3.1. remove urls_list_to_scrape[0]
            3.2. [scrape_url_list()]
            3.3. exit
     4. If url_to_scrape disallowed by Robots.txt then
            4.1. append url_to_scrape to urls_list_disallowed[]
            4.2. remove urls_list_to_scrape[0]
            4.3. [scrape_url_list()]
            4.4. exit
     5. If url_to_scrape domain not web_site_url domain then
            5.1. append url_to_scrape to urls_list_outside_domain[]
            5.2. remove urls_list_to_scrape[0]
            5.3. exit
     5. [scrape_url(url_to_scrape)]
     6. append url_to_scrape to urls_list_scraped[]
     7. remove urls_list_to_scrape[0]
     8. [scrape_url_list()]
     9. Exit


[DEF scrape_url(url_to_scrape)]
     1. If !url_to_scrape then exit
     2. Get links_list from url_to_scrape html content
     3. Append links_list to urls_list_to_scrape[]
     4. Exit
"""


def main():
    """."""

    os.system('cls')

    l_main_url = "https://www.debenhams.com"

    # driver = webdriver.Chrome(executable_path=chromedriver_path)
    # getlinks(driver, url)
    # print("EXITO!")

    l_scraper = MyWebScraper(l_main_url)
    # print(l_scraper.get_robot_url())
    # Load the DEBENHAMS site ROBOTS.TXT
    l_scraper.load_robot_file()

    # Just to check if ROBOTS.TXT is ok...
    # if l_scraper.get_robot_parser().allowed("https://www.debenhams.com/products/rui.php", "*"):
    #     print("OK!")
    # else:
    #     print("NOT OK!")

    # Initialize the url to scrape list
    # Adds the root url (ROBOTS.TXT host directive or indicated url) as the first element of the list
    l_scraper.initialize_list_url_to_scrape()

    # Scrapes the url list
    l_scraper.scrape_url_list()

    # TESTING - Date format to string
    # datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Export each array url scraped and array map url to corresponding csv
    with open("C:\\Rui Cruz\\Temp\\URL_SCRAPED_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".csv", "w", newline="") as l_output:   #, newline="\n", encoding="utf-8") as l_output:
        l_new_writer = csv.writer(l_output)
        for l_aux in l_scraper.v_urls_scraped:
            # Needs to be surrounded by "[]" because it's a string
            l_new_writer.writerow([l_aux])
        # l_new_writer.writerows([l_scraper.v_urls_scraped])

    # Export each array url scraped and array map url to corresponding csv
    with open("C:\\Rui Cruz\\Temp\\MAP_URL_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".csv", "w", newline="") as l_output:
        l_new_writer = csv.writer(l_output)
        for l_aux in l_scraper.v_map_list:
            # No need to be surrounded by "[]" because it is an array
            l_new_writer.writerow(l_aux)
        # l_new_writer.writerows([l_scraper.v_map_list])




#    p = Paises("/Europa/Quadro+Resumo/Alemanha-230971")
#
#    l_raw_site_content = p.get_raw_site_content()
#
#    l_data_content = p.get_data_content(l_raw_site_content, "table", "id", "QrTable")
#
#    p.transform_table_header_content(l_data_content)
#
#    p.transform_table_data_content(l_data_content)
#
#    print("*****  THE END  *****")




if __name__ == "__main__":
    main()
