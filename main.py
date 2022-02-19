from fastapi import FastAPI
import uvicorn

from tutorial import app01, app02, app03

app = FastAPI()

# 接下来🔛再请求 test01中的连接地址 就需要带上前缀了  tags代表了api中的标题
app.include_router(app01, prefix="/test1",tags=["请求参数和验证"])
app.include_router(app02, prefix="/test2",tags=["响应处理和FastAPI 配置"])
app.include_router(app03, prefix="/test3",tags=["FastAPI的依赖注入系统"])

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, debug=True, workers=1)

# coronavirus
# tutorial
