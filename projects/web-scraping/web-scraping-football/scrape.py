from bs4 import BeautifulSoup
from csv import writer
import requests
import os

urls = ["https://www.sofascore.com"]

for url in urls:
    headers = {'User-Agent': 'Mozilla/5.0'}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    
    with open("sofascore.csv", "a", encoding="utf-8") as csvfile:
        writer_csv = writer(csvfile)
        div = soup.find("div", id="main-container")
        print(div)
