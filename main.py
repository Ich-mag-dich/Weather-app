from fastapi.responses import FileResponse
from fastapi import FastAPI
app = FastAPI()


# 메인페이지 접속시 "/" 로 가능
# 정확히는 나중에 알아보기 -> 경로인가봄 ?
# 아래 세 줄이 템플릿 느낌

@app.get("/")
def svJoin():
    return FileResponse("./html/index.html")


@app.get("/data")
def svData():
    return {"hello": 1234}
