# uvicorn main:app --reload --host=0.0.0.0 --port=8000

from datetime import datetime
from fastapi.responses import FileResponse
from fastapi import FastAPI, Form, Request
import os

app = FastAPI()

# 메인페이지 접속시 "/" 로 가능
# 정확히는 나중에 알아보기 -> 경로인가봄 ? -> 맞네


def writeFile(ip_addr):
    # 밑에 'w' -> 파일 내용 초기화 후 작성
    # 'a' -> 파일 내용 유지 후 작성
    with open('./log_etc/get.txt', 'a', encoding='utf-8') as f:
        s = ip_addr
        f.write(f'{s}\n')


def readFile(ip_addr):
    with open('./log_etc/get.txt', 'r', encoding='utf-8') as r:
        lines = r.readlines()
        check_ip_bool = False
        for line in lines:
            if ip_addr in line:
                check_ip_bool = True
                break
        if check_ip_bool == False:
            return writeFile(ip_addr)


@app.get("/")
def svJoin(request: Request):
    nowTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(f"\n\033[1m{nowTime} \033[0m")
    client_host = request.client.host
    print(f"client_host: {client_host}")
    readFile(client_host)
    return FileResponse("./html/index.html")


@app.post("/send")
async def sendData(username: str = Form(), password: str = Form()):
    print(f"\033[1m\nusername: {username}, password: {password} \033[0m")
    return {"username": username, "password": password}
