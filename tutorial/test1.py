import datetime
from typing import Optional, List

from fastapi import APIRouter, Path, Query, Cookie, Header
from enum import Enum

from pydantic import BaseModel, Field
from datetime import date

app01 = APIRouter()

"""
Path Parameters  and Number validation 路径参数与数字验证验证
"""


@app01.get("/path/parameters")
async def path_params01():
    return {"message": "This is a message"}


@app01.get("/path/{parameters}")  # 函数的顺序 就是路由的顺序
async def path_params02(parameters):
    return {"message": f"This is a {parameters}"}


class CityName(str, Enum):
    BeiJing = "beijing china"
    ShangHai = "shanghai china"


# 还可以定义枚举类型
@app01.get("/enum/{city}")
async def latest(city: CityName):
    if city == CityName.BeiJing:
        return {"cityName": city, "count": 1111, "death": 10}
    elif city == CityName.ShangHai:
        return {"cityName": city, "count": 2222, "death": 22}


# 通过path path 传递路径  :path  代表 这个是个路径传值
@app01.get("path/{file_path:path}")
async def file_path(file_path: str):
    return {"filePath": f"{file_path}"}


# 验证参数
@app01.get("path_/{num}")
def path_params_verify(num: int = Path(..., title="Your number", description="不可描述", ge=1, le=10)):
    return num


"""
Query Parameters and String Validation 查询参数和字符串的验证
"""


# 给了参数值就是必填参数 没给就可填可不填
@app01.get("query")
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


# 布尔值的转换
@app01.get("query/bool/conversion")
def bool_conversion(params: bool = False):
    return f"{params}"


# 查询多个参数的列表
@app01.get("query/string/conversion")
def string_conversion(
        value: str = Query(..., min_length=8, max_length=16, regex="^a"),
        values: List[str] = Query(default=["v1", "v2"], alias="alias_name")
):
    return {"value": f"{value}", "values": f"{values}"}


"""Request Body and Field请求体和字段"""


class CityInfo(BaseModel):
    # example 是注解 的功能
    name: str = Field(..., example="BeiJing")
    country: str
    country_code: str = None
    country_population: int = Field(default=800, title="人口数量", description="国家的人口数量", ge=800)

    class Config:
        schema_extra = {
            "example": {
                "name": "shanghai",
                "country": "China",
                "country_code": "CN",
                "country_population": 1400000,
            }
        }


@app01.post("/request_body/city")
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.json()


"""
多参数的混合 path parameters+Query parameters 
"""


@app01.put("/request_body/city/{name}")
def mix_city_info(
        name: str,
        city01: CityInfo,
        city02: CityInfo,
        confirmed: int = Query(ge=0, description="确诊人数", default=0),
        death: int = Query(ge=0, description="死亡人数", default=0),
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(), city02.dict()


"""Request Body - Nested Models 数据格式嵌套的请求体"""


class Data(BaseModel):
    city: List[CityInfo] = None  # 这里就是定义 数据格式嵌套的请求体
    date: date  # 额外的数据类型 可以在官网查找到
    confirmed: int = Field(ge=0, default=0, description="确诊人数")
    death: int = Field(ge=0, default=0, description="死亡人数")
    recovered: int = Field(ge=0, default=0, description="治愈人数")


@app01.put("/request_body/nest")
def nested(data: Data):
    return data.json()


"""cookie 和 headers 参数"""


@app01.get("/cookie")
def cookie(cookie_id: Optional[str] = Cookie(None)):
    return {"cookie_id": cookie_id}


@app01.get("/header")
def header(user_agent: Optional[str] = Header(None), x_token: List[str] = None):
    return {"user_agent": user_agent, "x_token": x_token}
