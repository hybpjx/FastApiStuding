from typing import Optional, Union, List

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

app02 = APIRouter()

"""response model 响应模型"""


class UserInfo(BaseModel):
    user_name: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    user_name: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


users = {
    "user01": {"user_name": "zic1", "password": "1234555", "email": "hybpjx1@163.com"},
    "user02": {"user_name": "zic2", "password": "12345", "email": "hybpjx2@163.com", "mobile": "110"}
}


# response_model_exclude_unset=True 只封装 填入的值
@app02.post("/response_model", response_model=UserInfo, response_model_exclude_unset=False)
async def response_model(user: UserInfo):
    print(user.password)
    return users["user02"]


@app02.post(
    "/response_model/attributes",
    # response_model=UserInfo,
    # response_model=Union[UserInfo, UserOut]
    response_model = List[UserInfo],
    # response_model_include=["user_name", "email"],
    # response_model_exclude=["password"]
)
async def response_model_attr(user: UserInfo):
    # 可通过关键字删除密码  即使删除密码 依然可以成功
    # del user.password
    # 在使用  response_model = List[UserInfo] 时 需要返回一个列表
    return [user,user]
    # return user.dict()


