from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

app03 = APIRouter()

"""Dependencies 函数作为依赖项 创建和导入和声明依赖"""


async def common_parameters(q: Optional[str] = None, page: int = 1, limit: int = 10):
    return {"q": q, "page": page, "limit": limit}


@app03.get("/dependency01")  # 依赖的导入和声明
async def dependency01(commons: dict = Depends(common_parameters)):
    return commons


# 不区分 async 和 def 都可以调用
@app03.get("/dependency02")
def dependency02(commons: dict = Depends(common_parameters)):
    return commons


"""
classes as dependencies 类作为依赖性
"""

fake_items_db = [
    {
        "item_name": "Foo",
    },
    {
        "item_name": "Bar",
    },
    {
        "item_name": "Nav",
    },
]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 1, limit: int = 10):
        self.q = q
        self.page = page
        self.limit = limit


@app03.get("/classes_as_dependencies")
# 三种写法
# async def classes_as_dependencies(common: CommonQueryParams = Depends(CommonQueryParams)):
# async def classes_as_dependencies(common: CommonQueryParams = Depends()):
async def classes_as_dependencies(common=Depends(CommonQueryParams)):
    response = {}
    if common.q:
        response.update({"q": common.q})
    items = fake_items_db[common.page:common.page + common.limit]
    response.update({"items": items})
    return response


"""
Sub-dependencies 子依赖
"""


def query(q: Optional[str] = None):
    return q


def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if q:
        return q
    else:
        return last_query


@app03.get("/sub_dependency")
async def sub_dependency(final_query: str = Depends(sub_query, use_cache=True)):
    # use_ache表示 当有多个依赖有一个共同的子依赖时，每次request请求只会调用子依赖一次，多次调用将从缓存中调用。
    return {"sub_dependency": final_query}


"""
Dependencies in path operation decorators 路径操作装饰器中的多依赖
"""


async def verify_token(x_token: str = Header(...)):
    """没有返回值的子依赖"""
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")
    return x_token


async def verify_key(x_key: str = Header(...)):
    """有返回值的子依赖 但是返回值不会被调用"""
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
    return x_key


@app03.get("/dependency_in_path_operations", dependencies=[Depends(verify_token), Depends(verify_key)])
async def dependency_in_path_operations():
    return [
        {"user": "user01"},
        {"user": "user02"},
        {"user": "user03"},
    ]


"""
Global Dependencies 全局依赖
"""

# 使得全局都要 经过上述定义的两个以来 key和token
# app03 = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])


"""
Dependency with yield 带yield的依赖
"""


# 需要python 3.7 版本才支持，不然的话 需要安装很多的依赖，async-exit-stack async-generator
# 以下是伪代码

async def get_db():
    db = "db_connection"
    try:
        yield db
    finally:
        db.endswith("db_close")


async def dependency_a():
    dep_a = "generate_dep_a()"
    try:
        yield dep_a
    finally:
        dep_a.endswith("dep_a_close")


async def dependency_b(dep_a: Depends(dependency_a)):
    dep_b = "generate_dep_b()"
    try:
        yield dep_b
    finally:
        dep_b.endswith(dep_a)


async def dependency_c(dep_b: Depends(dependency_b)):
    dep_c = "generate_dep_c()"
    try:
        yield dep_c
    finally:
        dep_c.endswith(dep_b)
