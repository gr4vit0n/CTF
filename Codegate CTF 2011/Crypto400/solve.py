#!/usr/bin/env python

import base64
import re

pattern = r'GET[^\n]+$'
iv = None
pad = 0x10101010101010101010101010101010
cipher = None
fake_ivs = []

logfile = open('./crypto400.txt', 'r')

for line in logfile:
    greped = re.search(pattern, line).group()
    array = re.split(r'\s+', greped)
    status = array[-1]
    uri = array[1].lstrip('/')
    uri += '=' * (len(uri) % 4)
    decoded = base64.urlsafe_b64decode(uri).encode('hex')
    first = decoded[:32]
    second = decoded[32:]

    if(status=='200'):
        iv = int(first, 16)
        cipher = int(second, 16)
        print("[*] IV: 0x%032x" % iv)
        print("[*] Cipher Text: 0x%032x" % cipher)
    elif(status=='403'):
        fake_ivs.append(int(first, 16))
    else:
        pass

logfile.close()

print("[*] Fake IV: 0x%032x" % fake_ivs[-1])
print("[*] Padding: 0x%032x" % pad)
key = pad ^ fake_ivs[-1]
print("[+] Key Stream = (Fake IV) XOR Padding = 0x%032x" % key)
plain = key ^ iv
print("[+] Plain Text = (Key Stream) XOR IV = 0x%032x" % plain)
print("[+] FLAG: %s" % format(plain, 'x').decode('hex'))