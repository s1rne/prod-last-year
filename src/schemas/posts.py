from pydantic import BaseModel


class NewPostRequest(BaseModel):
    content: str
    tags: list[str]
