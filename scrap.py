from bs4 import BeautifulSoup as bs
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import time
import requests
import random

url = "http://www.rjb.csic.es/jardinbotanico/jardin/index.php?Cab=8&SubCab=548&len=en&Pag=549"
page = requests.get(url)
html = page.text
pattern = "<em.*?>.*?</em.*?>"
title_index = html.find("<em>")
start_index = title_index + len("<em>")
end_index = html.find("</em>")
em1 = html[start_index:end_index]

title_index = html.find("<em>")
start_index = title_index + len("<em>")
end_index = html.find("</em>")

em2=html[start_index:end_index]
print(em2)
