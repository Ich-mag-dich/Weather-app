# uvicorn main:app --reload --host=0.0.0.0 --port=80

from datetime import datetime
from fastapi.responses import FileResponse
from fastapi import FastAPI, Form
app = FastAPI()

# 메인페이지 접속시 "/" 로 가능
# 정확히는 나중에 알아보기 -> 경로인가봄 ? -> 맞네


@app.get("/")
def svJoin():
    nowTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(f'\n{nowTime}')
    return FileResponse("./html/index.html")


@app.post("/send")
async def sendData(username: str = Form(), password: str = Form()):
    print(f"username: {username}, password: {password}")
    return {"username": username, "password": password}
