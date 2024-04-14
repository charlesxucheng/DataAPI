from typing import List

from pydantic import BaseModel, json


class RouteConfig(BaseModel):
    path: str
    sql: str
    params: List[str] = []


def load_config() -> List[RouteConfig]:
    with open("./config.json", "r") as f:
        data = json.load(f)
    return [RouteConfig(**item) for item in data]
