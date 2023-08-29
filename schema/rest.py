from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RestRequest(BaseModel):
    action: str
    filter_by: Optional[Dict[str, Any]]
    order_by: Optional[str]
    limit: Optional[int]
    offset: Optional[int]


class BaseJsonResponse(BaseModel):
    status: str
    result: Any


class ProductsList(BaseJsonResponse):
    result: List[dict]


class CustomersList(BaseJsonResponse):
    result: List[dict]