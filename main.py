# uvicorn main:app --reload --host=0.0.0.0 --port=8000

from datetime import datetime
from fastapi.responses import FileResponse
from fastapi import FastAPI, Form, Request
import os
import urllib3
import ast
import requests

app = FastAPI()

strColor = "\033[1;31;40m"
strBold = "\033[1m"
strNormal = "\033[0m"

# 메인페이지 접속시 "/" 로 가능
# 정확히는 나중에 알아보기 -> 경로인가봄 ? -> 맞네


def writeFile(ip_addr, country):
    # 밑에 'w' -> 파일 내용 초기화 후 작성
    # 'a' -> 파일 내용 유지 후 작성
    with open('./log_etc/get.txt', 'a', encoding='utf-8') as f:
        s = f"{ip_addr} ({country})"
        f.write(f'{s}\n')


def readFile(ip_addr, country):
    with open('./log_etc/get.txt', 'r', encoding='utf-8') as r:
        lines = r.readlines()
        check_ip_bool = False
        for line in lines:
            if ip_addr in line:
                check_ip_bool = True
                break
        if check_ip_bool == False:
            return writeFile(ip_addr, country)


def get_location(ip_addr):
    response = requests.get(f'https://ipapi.co/{ip_addr}/json/').json()
    location_country = response.get("country_name")
    return location_country

# bold -> \033[1m


@app.get("/")
async def svJoin(request: Request):
    nowTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(f"\n{strBold}{strColor}Time{strNormal}: {nowTime}")
    client_host = request.client.host
    loc_country = get_location(client_host)
    print(
        f"{strBold}{strColor}Client_host{strNormal}: {client_host} \n{strBold}{strColor}Country{strNormal}: {loc_country}")
    readFile(client_host, loc_country)
    return FileResponse("./html/index.html")


@app.post("/send")
async def sendData(username: str = Form(), password: str = Form()):

    print(f"{strBold}\nusername: {username}, password: {password} {strNormal}")
    return {"username": username, "password": password}
