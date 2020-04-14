# -*- coding: utf-8 -*-
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Secret Sign
import time
import hmac
import hashlib
import base64
import urllib.parse

from account import account

# API Doc: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
class dingdingMessager:

    def __init__(self):
        self.account = account()
        self.urlPrefix = u'https://oapi.dingtalk.com/robot/send?access_token={0}'.format(self.account.dingdingToken)
        self.headers = \
        {   \
            'Content-Type': 'application/json',\
        }

    def generateSign(self):
        timestamp = str(round(time.time() * 1000))
        secret = self.account.dingdingSecret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # print(timestamp)
        # print(sign)
        return {'ts': timestamp, 'sign': sign}

    def send(self, text):
        dict = {'msgtype':'text'}
        params = self.generateSign()
        dict['text'] = {'content': text}
        data = json.dumps(dict)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        url = self.urlPrefix + '&timestamp={0}&sign={1}'.format(params['ts'], params['sign'])
        response = requests.post(url, verify=False, headers=self.headers, data=data)
        if response.status_code != 200:
            print('[ERROR] 钉钉机器人发送失败：{0}'.format(response.text))
        else:
            jsonData = json.loads(response.text)
            jsonData['text'] = text
            print(jsonData)
        #response.text = \
        #{  \
        #	"errcode": 0,   \
        #	"errmsg": "ok"  \
        #}
        
if __name__ == "__main__":
    dingdingMessager().send(u'试试随便发点什么')