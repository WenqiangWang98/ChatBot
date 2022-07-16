from bs4 import BeautifulSoup as bs
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import time
import requests
import random
import re
import unicodedata
import csv
name = []
fam = []
location = []
page = []
page.append( requests.get(
    "http://www.rjb.csic.es/jardinbotanico/jardin/index.php?Cab=8&SubCab=548&len=en&Pag=549"))
pag1 = "http://www.rjb.csic.es/jardinbotanico/jardin/index.php?Cab=8&SubCab=548&len=en&Pag=549&Caracter="

for i in range(ord('B'), ord('Z')+1):
    page.append(requests.get(pag1+chr(i)))
for i in range(len(page)):

    soup = bs(page[i].content)
    quotes = [unicodedata.normalize("NFKD", i.text)
              for i in soup.find_all(id="descripcion")]

    for i in range(len(quotes)):
        nam = quotes[i][1:quotes[i].find("(")].lower()
        name.append(nam.strip())
        fam.append(quotes[i][quotes[i].find(": ")+2:quotes[i].rfind(")")-1].lower())
        loc = (quotes[i][quotes[i].find("n:")+3:quotes[i].rfind("\n")])
        loc = loc.replace("video", '')
        loc = loc.replace("foto", '')
        loc = loc.replace("Foto", '')
        loc=loc.lower()
        location.append(loc.strip())

with open('datos.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(name)):
        spamwriter.writerow([name[i]] + [fam[i]] + [location[i]])

