from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from vserver import services
from vserver.api import deps
from vserver.schemas.video import Video, VideoCreate

api_router = APIRouter()


@api_router.post('', response_model=Video)
def import_video(
    db: Session = Depends(deps.get_db),
    *,
    video_in: VideoCreate,
) -> Any:
    """
    Import video.
    """
    video = services.video.create(db, obj_in=video_in)
    return video


@api_router.get('/{video_id}', response_model=Video)
def find_video(
    video_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific video by id.
    """
    video = services.video.get(db, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail='Video not found')
    return video


@api_router.get('/{video_id}/urls')
def get_video_urls(
    video_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific video by id.
    """
    video = services.video.get(db, video_id)
    return video.urls
