import time

from fastapi import FastAPI,Request
import uvicorn

from coronavirus import application
from tutorial import app01, app02, app03,app04,app05,app06
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI Tutorial and Coronavirus Tracker API Docs ",
    description="新管病毒 疫情跟踪器 API接口文档",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redocs",
    # dependencies=[Depends(verify_token), Depends(verify_key)]
)

from fastapi.staticfiles import StaticFiles

# mount 表示 将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path="/static", app=StaticFiles(directory="./coronavirus/static"), name="static")
#
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from fastapi.exceptions import HTTPException
# from starlette.exceptions import HTTPException as star_HTTPException
# @app.exception_handler(star_HTTPException)  # 重写异常处理
# async def http_exception_handler(request, exc):
#     """
#     :param request: 这个参数不能省
#     :param exc:
#     :return: 只是把原本是Json的response 转变成文本的response
#     """
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.exception_handler(RequestValidationError)  # 重写请求验证的处理器
# async def validation_exception_handler(request, exc):
#     """
#     :param request: 这个参数不能省
#     :param exc:
#     :return:
#     """
#     return PlainTextResponse(str(exc), status_code=400)

# 拦截http请求
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):  # call_next将接收request请求做为参数
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)  # 添加自定义的以“X-”开头的请求头
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 接下来🔛再请求 test01中的连接地址 就需要带上前缀了  tags代表了api中的标题
app.include_router(app01, prefix="/test1", tags=["请求参数和验证"])
app.include_router(app02, prefix="/test2", tags=["响应处理和FastAPI 配置"])
app.include_router(app03, prefix="/test3", tags=["FastAPI的依赖注入系统"])
app.include_router(app04, prefix="/test4", tags=["安全 认证与授权"])
app.include_router(app05, prefix="/test5", tags=["数据库文件设计"])
app.include_router(app06, prefix='/test6', tags=['中间件、CORS、后台任务、测试用例'])
app.include_router(application, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])

if __name__ == '__main__':
    # uvicorn.run("main:app", reload=True, debug=True, workers=1)
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, debug=True, workers=10)

# coronavirus
# tutorial
