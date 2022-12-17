from fastapi import FastAPI

from vserver.api.v1.api import api_router

app = FastAPI(openapi_url="")

app.include_router(api_router, prefix='/v1')
