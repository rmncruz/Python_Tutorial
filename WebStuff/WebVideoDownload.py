
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
	l_r = requests.get(p_archive_url)

	# create beautiful-soup object
	l_soup = BeautifulSoup(l_r.content, 'html5lib')

	# find all links on web-page
	l_links = l_soup.findAll('a')

	# filter the link sending with .mp4
	l_video_links = [p_archive_url + link['href']
                for link in l_links if link['href'].endswith('mp4')]

	return l_video_links



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
	with open("C:\\Users\\rui.m.da.cruz\\OneDrive - Accenture\\RCruz\\Tech\\Python\\Tutorial\\LixoWeb\\" + l_file_name, 'wb') as f:
		for chunk in l_r.iter_content(chunk_size=1024*1024):
			if chunk:
				f.write(chunk)

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


if __name__ == "__main__":

	# sys.stdout.write("Hello World!")

	# getting all video links
	l_video_links = get_video_links(archive_url)

    # Remove duplicated values from list
	l_video_links2 = remove_duplicated_values(l_video_links)

	# download all videos
	download_video_series(l_video_links2)
