from typing import Optional, Union, List

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr
from starlette import status

app02 = APIRouter()

"""response model 响应模型"""


class UserIn(BaseModel):
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
@app02.post("/response_model", response_model=UserIn, response_model_exclude_unset=False)
async def response_model(user: UserIn):
    print(user.password)
    return users["user02"]


@app02.post(
    "/response_model/attributes",
    # response_model=UserInfo,
    # response_model=Union[UserInfo, UserOut]
    response_model=List[UserIn],
    # response_model_include=["user_name", "email"],
    # response_model_exclude=["password"]
)
async def response_model_attr(user: UserIn):
    # 可通过关键字删除密码  即使删除密码 依然可以成功
    # del user.password
    # 在使用  response_model = List[UserInfo] 时 需要返回一个列表
    return [user, user]
    # return user.dict()


# @app02.post("/file")
# async def fileobj(file: bytes = File(...)):
@app02.post("/file")  # 上传多个文件
async def fileobj(file: List[bytes] = File(...)):
    """ 由于文件读写 是由bytes 读取 所以适合小内存多文件"""
    return {"file_size": len(file)}


@app02.post("/upload_file")
async def upload_file(files: List[UploadFile] = File(...)):
    """
    使用 upload_file的优势：
    1. 文件储存在内从中 当文件大于一个阀值 就写入磁盘总
    2. 适用于图片 视频 等
    3. 可以获取上传文件多元数据 内存 ，大小 上传时间 等
    4. 有文件对象多异步接口
    5. 上传多是python对象 由 read write 等方法
    :param files:
    :param file:
    :return:
    """
    for file in files:
        content = await file.read()
        print(content)

    return {"file_name": files[1].filename, "file_content_type": files[0].content_type}


"""
见 main.py FastApi 项目的静态文件配置
"""

"""
Path Operation Configuration 路径操作配置
"""


@app02.post(
    "/path_operation_configuration",
    response_model=UserOut,
    # tags=['path','operation','configuration'],# 这个Tags 和主程序中的一样 会显示在API文档中
    summary="this is a summary",
    description="this is a description",
    response_description="this is a response description",
    # deprecated=True,# 表示这个接口已经废弃
    status_code=status.HTTP_200_OK,
)
async def path_operation_configuration(user: UserIn):
    """
    Path Operation Configuration 路径操作配置
    :param user: 用户信息
    :return: 返回结果
    """
    return user.dict()


"""
见 main.py FastAPI 应用的配置常用项
"""

"""
Handing Error 错误处理
"""


@app02.get("/http_exception", )
async def http_exception(city: str):
    if city != "Bei Jing":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City Not Found",
                            headers={"X-Error": "error"})
    return {"city": city}


"""
重写错误逻辑 见 main.py
"""


@app02.get("/overwrite_http_exception")
async def overwrite_http_exception(city_id: int):
    if city_id == 1:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="Nope I dont like 1",
                            headers={"X-Error": "error"})
    return {"city_id": city_id}
