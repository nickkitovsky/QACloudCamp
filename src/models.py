from pydantic import BaseModel, Field, StrictStr


class Post(BaseModel):
    user_id: int = Field(alias='userId')
    id: int
    title: StrictStr
    body: StrictStr


class Response(BaseModel):
    status_code: int
    body: list | dict
