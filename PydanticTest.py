from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, ValidationError, constr
from datetime import datetime, date


class User(BaseModel):
    id: int  # 必填字段
    name: str = "John Snow"  # 有默认值 选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # 列表中元素是int 类型 或者直接转换成int类型


external_data = {
    "id": "123",
    "name": "",
    "signup_ts": "2022-12-22 12:22",
    "friends": [1, 2, "3"]
}
print("\033[31m1. --校验数据处理--\033[0m")
user_ex = User(**external_data)
print(user_ex.id)
print(user_ex.friends)
print(repr(user_ex.signup_ts))
print(dict(user_ex))

print("\033[31m2. --校验失败处理--\033[0m")

try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, "not number"])

except ValidationError as e:
    print(e.json())

print("\033[31m3. --模型类的属性和方法--\033[0m")
# 字典格式
print(user_ex.dict())
# json 格式
print(user_ex.json())
# 浅拷贝
print(user_ex.copy())
# 传入对象解析
print(User.parse_obj(obj=external_data))
# 直接解析原生数据
print(User.parse_raw('{"id": "123","name": "","signup_ts": "2022-12-22 12:22","friends": [1, 2, "3"]}'))
# 解析文件
path = Path("pydantic.json")
path.write_text('{"id": "123","name": "","signup_ts": "2022-12-22 12:22","friends": [1, 2, "3"]}')
print(User.parse_file(path))

# 格式更多更全
print(User.schema())
print(User.schema_json())

# 不会报错
user_data = {"id": "error", "name": "", "signup_ts": "2022-12-22 12:22", "friends": [1, 2, "3"]}
# 不校验数据 直接创建模型类 不建议使用这种
print(User.construct(**user_data))

# 查看字段顺序 # 如果都定义了类型 那么顺序就不会乱
print(User.__fields__.keys())

print("\033[31m4. --递归模型--\033[0m")


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]


dog = Dog(birthday=date.today(), weight=6.1, sound=[{"sound": "wang wang ~"}, {"sound": "miao miao ~"}])
print(dog.json())

print("\033[31m5. --ORM模型：从类实例创建符合ORM对象的实例--\033[0m")

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = "CompanyOrm"
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, unique=True, nullable=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


# pydantic  格式化
class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


com_orm = CompanyOrm(
    id=123,
    public_key="foobar",
    name="Testing",
    domains=["example", "github.com"]
)

print(CompanyMode.from_orm(com_orm))