import requests
from bs4 import BeautifulSoup
import re

def get_links(url):
    r = requests.get(url)
    sp = BeautifulSoup(r.text, 'html.parser')
    links = sp.select('td.cellinside a')
    return [link.attrs['href'] for link in links]

def download_file(download_url, file_name=''):
    req = requests.get(download_url)
    try:
        if file_name:
            pass
        else:
            file_name = req.url[download_url.rfind('/')+1:]
    
        with open(file_name, 'wb') as f:
           for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return file_name
    except Exception as e:
        print(e)
        return None

# Scrape all the download links
links = get_links('https://vincentarelbundock.github.io/Rdatasets/datasets.html')

# Retrieve links for csv file only
csv_lst = []
ct = 0
for link in links:
    link = re.findall('^https://\S+csv', link)
    if len(link) < 1:
        continue
    else:
        csv_lst.append(link[0])
        ct += 1
print('retrieved', ct, 'links')

# Write retrieved links into atxt file
with open('csv_to_download.txt', 'w') as f:
    for d_link in csv_lst:
        d_link = d_link + '\n'
        f.write(d_link)
    print('txt file downloaded')

# Download a specific file named 'movielens.csv' from the links recorded in the txt file previously
with open('csv_to_download.txt') as f:
    for url in f:
        url = re.findall('^https://\S+movielens\.csv', url)
        if len(url) < 1:
            continue
        else:
            to_download = url[0]
    download_file(to_download)
    print('csv file downloaded')



