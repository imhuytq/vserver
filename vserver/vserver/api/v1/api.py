from fastapi import APIRouter

from vserver.api.v1.endpoints import videos, browse

api_router = APIRouter()
api_router.include_router(videos.api_router, prefix='/videos')
api_router.include_router(browse.api_router, prefix='/browse')
