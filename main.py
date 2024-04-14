from fastapi import FastAPI, Path
from sqlalchemy.orm import Session

from route_config import RouteConfig, load_config

app = FastAPI()
routes = {}


def register_route(route_config: RouteConfig):
    # Build regular expression with capture groups for each parameter
    pattern = route_config.path.replace(":<param>", r"(?P<" + r"\w+>" + r")")
    for param in route_config.params:
        pattern = pattern.replace(":" + param, r"(?P<" + param + r")")

    # Define route handler function
    async def route_handler(db: Session, **kwargs):
        # Use f-strings for parameter insertion
        sql = route_config.sql.format(**kwargs)
        result = db.execute(sql).fetchone()
        return {"data": result}  # Example response with retrieved data

    # Add route with path pattern and handler function
    app.get(pattern)(route_handler)
    routes[route_config.path] = route_handler


# Load configuration and register routes
for config in load_config():
    register_route(config)
