# uvicorn main:app --reload --host=0.0.0.0 --port=8000

from datetime import datetime
import sys
from pip import main
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi import FastAPI, Form, Request
import os
import requests
import json
from fastapi.templating import Jinja2Templates

print(10**4)
sys.setrecursionlimit(10**4)

app = FastAPI()

strColor = "\033[1;31;40m"
strBold = "\033[1m"
strNormal = "\033[0m"

header = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'

}
# 메인페이지 접속시 "/" 로 가능
# 정확히는 나중에 알아보기 -> 경로인가봄 ? -> 맞네

# bold -> \033[1m


@app.get("/")
async def indexJoin():
    return FileResponse("./html/index.html")

favicon_path = './favicon.ico'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.post("/send")
async def sendData(username: str = Form(), password: str = Form()):

    print(f"{strBold}\nusername: {username}, password: {password} {strNormal}")
    return {"username": username, "password": password}


def getKey():
    with open("./key/key.txt", "r", encoding='utf-8') as r:
        return r.readline()


def getWeather(loc="Buyeo"):
    url1 = f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={getKey()}&units=metric"
    req = requests.get(url=url1, headers=header)
    return(req.text)


# def getLatLon():
#     req = requests.get(
#         url=f"http://api.openweathermap.org/geo/1.0/direct?q=Seoul&limit=1&appid={getKey()}", headers=header)
#     #res = req.urlopen(req)
#     gotContent = req.content
#     latlonJson = json.loads(gotContent)
#     # print(gotContent)
#     # print(latlonJson[0]["lat"])
#     # print(latlonJson[0]["lon"])
#     return getWeather(latlonJson[0]["lat"], latlonJson[0]["lon"])


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# class datesWeather(self, todayData: json, data: json, request: any):
#     def __init__(self):
def get5daysWeather(loc="Buyeo"):
    url1 = f"https://api.openweathermap.org/data/2.5/forecast?q={loc}&appid={getKey()}&units=metric"
    req = requests.get(url=url1, headers=header)
    # print(len(req.json()["list"]))
    # print(req.json()["list"][0])
    return req.text


def returnFunc(data: json, request: any, id="Buyeo"):
    datas = {
        "request": request,
        "id": data["name"],
        "weatherIcon": data["weather"][0]["icon"],
        "nowTemp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "pressure": data["main"]["pressure"],
        "humidity": data["main"]["humidity"],
        "windSpeed": data["wind"]["speed"],
        "nowTime": datetime.fromtimestamp(data["dt"]).strftime("%H시 %M분"),
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H시 %M분"),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H시 %M분")
    }

    daysForecast = json.loads(get5daysWeather(id))

    # print(daysForecast["list"][0]["weather"][0]["icon"])
    dts = []
    feels = []
    icons = []
    temps = []
    hums = []
    for i in range(0, 41):
        try:
            dts.append(datetime.fromtimestamp(
                daysForecast["list"][i]["dt"]).strftime("%m.%d %H시"))
            icons.append(daysForecast["list"][i]["weather"][0]["icon"])
            hums.append(daysForecast["list"][i]["main"]["humidity"])
            temps.append(daysForecast["list"][i]["main"]["temp"])
            feels.append(daysForecast["list"][i]["main"]["feels_like"])
        except:
            print("error")
            continue
    datas["dt"] = dts
    datas["feels"] = feels
    datas["icons"] = icons
    datas["temps"] = temps
    datas["hums"] = hums
    # print(datas.get("dt"))
    # print(i, len(datas))
    return datas


@app.get("/test", response_class=HTMLResponse)
async def testPage(request: Request):
    data = json.loads(getWeather())
    return f"""
        <h1> 
            {returnFunc(data,request)}
        </h1>
    """


@app.get("/weather", response_class=HTMLResponse)
async def baseWeatherPage(request: Request):
    data = json.loads(getWeather())
    return templates.TemplateResponse("weather.html", returnFunc(data, request))


@app.get("/weather/{id}", response_class=HTMLResponse)
async def weatherPage(request: Request, id: str):
    data = json.loads(getWeather(id))
    return templates.TemplateResponse("weather.html", returnFunc(data, request, id))
