from bs4 import BeautifulSoup, SoupStrainer
import requests
import os
import shutil

def get_folders(url="http://www.incline.iag.usp.br/data/disciplinaPOS/2020/material_de_apoio/"):
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data)
    folders = []
    for link in soup.find_all('a'):
        links = link.get('href')
        if "08" in links:
            folders.append(links)
    return(folders)


def create_folders(path):
    #path = "C:\\Users\\artur\\OneDrive\\Mestrado\\Disciplinas\\AGM5832 - Mudanças climáticas e suas interdisciplinaridades\\Teste"
    folders = get_folders()
    os.chdir(path)
    files = os.listdir()
    for folder in folders:
        if folder[:-1] not in files:
            os.mkdir(folder[:-1])

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename

def download_content(path, url="http://www.incline.iag.usp.br/data/disciplinaPOS/2020/material_de_apoio/"):
    folders = get_folders()
    for folder in folders:
        folder_url = url + folder
        folder_page = requests.get(folder_url)
        folder_data = folder_page.text
        folder_soup = BeautifulSoup(folder_data)
        os.chdir(path + "\\" + folder)
        files_in_folder = os.listdir()
        for link in folder_soup.find_all('a'):
            folder_link = (link.get('href'))
            folder_link.replace(" ", "_")
            if "." in folder_link:
                file_to_download = folder_link.replace("%20", " ")
                if file_to_download not in files_in_folder:
                    link_to_download = folder_url + file_to_download
                    download = download_file(link_to_download)



