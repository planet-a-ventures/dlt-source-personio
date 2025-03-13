from pydantic import BaseModel


class MyBaseModel(BaseModel):
    pass


class MyAuthBaseModel(MyBaseModel):
    pass


class MyPersonnelBaseModel(MyBaseModel):
    pass


class MyRecruitingBaseModel(MyBaseModel):
    pass
