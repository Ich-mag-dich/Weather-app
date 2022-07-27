from fastapi import FastAPI
app = FastAPI()


# 메인페이지 접속시 "/" 로 가능
# 정확히는 나중에 알아보기
@app.get("/")
def svJoin():
    return "hello"
