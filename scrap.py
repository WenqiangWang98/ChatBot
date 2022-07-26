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
page = requests.get("https://rjb.csic.es/el-jardin/las-plantas-del-jardin/arboles/")
soup = bs(page.content)
quotes = [unicodedata.normalize("NFKD",i.text) for i in soup.find_all("td")]

name=[]
fam=[]
location=[]
for i in range(len(quotes)):
    buff=quotes[i]
    if i%4==1:
        name.append(buff)
    elif i%4==2:
        fam.append(buff)
    elif i%4==3:
        location.append(buff)

with open('datos.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(name)):
        spamwriter.writerow([name[i]] + [fam[i]] + [location[i]])

