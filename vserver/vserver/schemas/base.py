from pydantic import BaseModel
from stringcase import camelcase


class Base(BaseModel):
    class Config:
        @classmethod
        def alias_generator(cls, string: str) -> str:
            return camelcase(string)


class InDBBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True
