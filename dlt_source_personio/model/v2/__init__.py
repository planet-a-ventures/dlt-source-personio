from pydantic import BaseModel


class MyBaseModel(BaseModel):
    pass


class MyAuthBaseModel(MyBaseModel):
    pass


class MyPersonBaseModel(MyBaseModel):
    pass
