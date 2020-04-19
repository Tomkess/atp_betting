# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:06:03 2020

@author: Peter.Tomko
"""

## ----- Loading modules ----- ##
from urllib.request import urlopen
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO
import os

## ----- Create Folder Structure for Downloaded Data ----- ##
path = "C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Downloaded Data"
def createFolder(directory):
    """
    Input - name of the folder in which the data are downlaoded
    Output - created folder
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

# - Create Folders for Downloaded Data
createFolder(path)
createFolder(path + '/men')
createFolder(path + '/women')

# - Create Folders for Generated Data
createFolder("C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data")

## ----- Get Initial Website ----- ##
page = urlopen('http://www.tennis-data.co.uk/alldata.php')
soup = BeautifulSoup(page, 'html.parser')

## ----- Get Links to all files ----- #
all_obj = soup.find_all("a")
files_links = []
for link in all_obj:
    href_obj = str(link['href'])
    if "zip" in href_obj:
        files_links.append(link['href'])

## ----- Download all zip files ----- ##
def downloadZipData(links_list, web_url, path_input):
    """
    Input - links that are downloaded from website
    Output - xls files stored in the path_input directory
    """
    for i_link in links_list:
        zipurl = web_url + '/' + i_link
        
        if "w" not in i_link:
            with urlopen(zipurl) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(path_input + '/men')

        if "w" in i_link:
            with urlopen(zipurl) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(path_input + '/women')

                    
downloadZipData(files_links, 'http://www.tennis-data.co.uk', path)