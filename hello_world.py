from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None  # 与bool值最大的区别是可以不传 默认是null


# @app.get("/")
# def hello_world():
#     return {"hello": "world"}
#
#
# @app.get("/city/{city}")
# def getCity(city: str, query_string: Optional[str] = None):
#     return {"city": city, "query_string": query_string}
#
#
# @app.put("/cityInfo/{city}")
# def request(city: str, CityInfo: CityInfo):
#     return {"city": city, "province": CityInfo.province, "country": CityInfo.country,
#             "is_affected": CityInfo.is_affected}

@app.get("/")
async def hello_world():
    return {"hello": "world"}


@app.get("/city/{city}")
async def getCity(city: str, query_string: Optional[str] = None):
    return {"city": city, "query_string": query_string}


@app.put("/cityInfo/{city}")
async def request(city: str, CityInfo: CityInfo):
    return {"city": city, "province": CityInfo.province, "country": CityInfo.country,
            "is_affected": CityInfo.is_affected}
