from pydantic import BaseModel


class AddFriendRequest(BaseModel):
    login: str
