from pydantic import BaseModel


class MyBaseModel(BaseModel):
    pass


class MyAuthBaseModel(MyBaseModel):
    pass


class MyPersonBaseModel(MyBaseModel):
    pass


class MyEmploymentBaseModel(MyBaseModel):
    pass


class MyErrorsBaseModel(MyBaseModel):
    pass
