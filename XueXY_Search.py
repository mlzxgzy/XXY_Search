#!/usr/bin/env python3
import getpass
import json
import requests
import os
import sys

configFile = "config.json"
# -=-=-=-=-=-=-=-=-=-=-=-=-=
if os.path.exists(configFile):
    config = open(configFile, "r")
else:
    config = open(configFile, "x")
configContent = "".join(config.readlines())
if configContent == "":
    configContent = "{}"
configJson: dict = json.loads(configContent)
config.close()
# -=-=-=-=-=-=-=-=-=-=-=-=-=
if configJson.get("api_token") == None:
    account = input("请输入账户: ")
    password = getpass.getpass("请输入密码: ")

    ret = requests.post("https://app.51xuexiaoyi.com/api/v1/login",
                        timeout=2,
                        json={"username": account, "password": password}
                        )
    if ret.status_code != 200:
        print("程序出现错误,请查看是否有更新!")
        exit(0)
    retJson = ret.json()
    if retJson["code"] != 200:
        print(retJson["msg"])
        exit(0)
    configJson = retJson["data"]
# -=-=-=-=-=-=-=-=-=-=-=-=-=
ret = requests.post("https://app.51xuexiaoyi.com/api/v1/userInfo",
                    timeout=2,
                    headers={"token": configJson["api_token"]}
                    )
retJson = ret.json()
if retJson["code"] != 200:
    print(retJson["msg"])
    os.remove(configFile)
    exit(0)
print("验证登陆成功!")
# -=-=-=-=-=-=-=-=-=-=-=-=-=
config = open(configFile, "w+")
configContent = json.dumps(configJson)
config.write(configContent)
config.close()
# -=-=-=-=-=-=-=-=-=-=-=-=-=
question = input("请输入问题: ")
ret = requests.post("https://app.51xuexiaoyi.com/api/v1/searchQuestion",
                    timeout=2,
                    headers={"token": configJson["api_token"],
                             "app-version": "1.0.6"},
                    json={"keyword": question}
                    )
retJson = ret.json()
print(retJson["msg"])
if retJson["code"] != 200:
    exit(0)
quesJson = retJson["data"]
for tmp in quesJson:
    print("问题: " + tmp["q"])
    print("答案: " + tmp["a"])
    print()
