import decimal
import datetime
import os
import requests
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict


''' 
URL of the archive web-page which provides link to 
all video lectures. It would have been tiring to 
download each video manually. 
In this example, we first crawl the webpage to extract 
all the links and then download videos. 
'''


# specify the URL of the archive here
archive_url = "http://www-personal.umich.edu/~csev/books/py4inf/media/"


def get_video_links(p_archive_url):
	""" Obtains the video links within the url provided """
	
	# create response object
	# v_r = requests.get("http://www-personal.umich.edu/~csev/books/py4inf/media/")
	v_r = requests.get(p_archive_url)

	# create beautiful-soup object
	v_soup = BeautifulSoup(v_r.content, "html5lib")

	# find all links on web-page
	v_links = v_soup.findAll('a')

	# filter the link sending with .mp4
	v_video_links = [p_archive_url + link['href']
                for link in v_links if link['href'].endswith('mp4')]

	return v_video_links



def download_video_series(video_links):
	'''iterate through all links in video_links and download them one by one'''

	for link in video_links:
		download_video(link)

	print("All videos downloaded!")
	return



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
	# Windows version
	# with open("C:\\Users\\rui.m.da.cruz\\OneDrive - Accenture\\RCruz\\Tech\\Python\\Tutorial\\LixoWeb\\" + v_file_name, 'wb') as f:
	# Mac version
	with open("/Users/rcruz/Development/Lixo/" + v_file_name, 'wb') as f:
		for chunk in v_r.iter_content(chunk_size=1024*1024):
			if chunk:
				f.write(chunk)

			v_chunk_sum += len(chunk)

			if v_chunk_sum > v_display_limit:
				os.system("cls")  # Clears the terminal
				display_download_info(v_file_name, v_content_length_byte, v_chunk_sum, v_start_time)
				v_display_limit += 100000

	print(v_file_name, "downloaded!")
	return



def remove_duplicated_values(p_originav_list):
    """ Removes the duplicated values from the provided list.
	    The output list values order might not be the same as the provided list values order """

    v_list_without_duplicated_values = list(set(p_originav_list))
    return v_list_without_duplicated_values



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


if __name__ == "__main__":

	# sys.stdout.write("Hello World!")

	# getting all video links
	v_video_links = get_video_links(archive_url)

    # Remove duplicated values from list
	v_video_links2 = remove_duplicated_values(v_video_links)

	# download all videos
	download_video_series(v_video_links2)
