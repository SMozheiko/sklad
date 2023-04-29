from typing import Optional, List

from pydantic import BaseModel
from enum import Enum

from database.models import Manager


class Method(str, Enum):
    get = 'get'
    post = 'post'


class Request(BaseModel):
    method: Method
    action: str
    params: Optional[dict]
    data: Optional[dict]
    user: Optional[Manager]

    class Config:
        arbitrary_types_allowed = True


class Response(BaseModel):
    header: Optional[str]
    tag: str
    html: str
    errors: List[str] = []
