import requests
import time
import random
import hashlib
import json
import pandas as pd
import csv
from aaa import WebFanyi as WebFanyi

# 翻译接口地址 "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"   translate_o 注意去掉 _o
class Youdao:
    def __init__(self, query):
        self.url = "https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.query = query
        self.headers = {
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Cookie": "OUTFOX_SEARCH_USER_ID=-1980470297@106.2.43.13; OUTFOX_SEARCH_USER_ID_NCOO=1063307492.9706801; UM_distinctid=168d63e2704c65-081d34ab71dc8e-10346654-13c680-168d63e2705586; JSESSIONID=aaa4lQm4WWe_o7Kds1IRw; ___rl__test__cookies=1558598655197"
        }

    # 生成ts字段结果
    def getTs(self):
        ts = str(int(time.time() * 1000))
        return ts

    # 生成salt字段结果
    def getSalt(self, ts):
        salt = ts + str(random.randint(0, 10))
        return salt

    # 生成sign加密字段结果
    def getSign(self, salt):
        md5 = hashlib.md5()
        encryption = "fanyideskweb" + self.query + salt + "@6f#X3=cCuncYssPsuRUE"
        md5.update(encryption.encode("utf-8"))
        sign = md5.hexdigest()
        return sign

    # 向接口发送post请求
    def sendRequest(self, data):
        response = requests.post(self.url, headers=self.headers, data=data).content.decode("utf-8")
        return response

    # 解析返回的数据
    def parse(self, response):
        response = json.loads(response)
        print(response)
        #result = response["translateResult"][0][0]["tgt"]
        result = response["trans_result"]['data'][0]["dst"]
        #print(result)
        return str(result)

    def run(self):
        # 分别获取ts,salt,sign加密字段字段
        ts = self.getTs()
        salt = self.getSalt(ts)
        sign = self.getSign(salt)
        # 准备发送post请求的字段
        data = {
            "i": self.query,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "ts": ts,
            "bv": "fdac15c78f51b91dabd0a15d9a1b10f5",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_CLICKBUTTION",
        }
        

        # 发送请求获取数据
        response = self.sendRequest(data)
        # 解析得到的数据
        return self.parse(response)


if __name__ == '__main__':
    

    #读取第一列、第二列、第四列
    df = pd.read_excel('TaskDataset.xlsx',sheet_name='Sheet1',usecols=[0])
    data = df.values
    
    ans = []
    for i in data:
        res = WebFanyi(str(i)).run()
        ans.append([str(i), str(res)])
        time.sleep(10)    
    
    with open('ans1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in ans:
            writer.writerow(row)