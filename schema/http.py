from typing import Optional, List

from pydantic import BaseModel
from enum import Enum


class Method(str, Enum):
    get = 'get'
    post = 'post'


class Request(BaseModel):
    method: Method
    action: str
    params: Optional[dict]
    data: Optional[dict]


class Response(BaseModel):
    tag: str
    html: str
    errors: List[str] = []