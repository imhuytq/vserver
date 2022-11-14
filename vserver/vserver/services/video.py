import base64
import json
from typing import Optional

from sqlalchemy.orm import Session
from ulid import ULID

from .base import Base
from vserver.core.celery_app import celery_app
from vserver.models.video import Video as ModelVideo
from vserver.schemas.video import VideoCreate, VideoUpdate


class Video(Base[ModelVideo, VideoCreate, VideoUpdate]):
    def get(self, db: Session, id: str | bytes | ULID) -> Optional[ModelVideo]:
        try:
            if isinstance(id, str):
                id = ULID.from_str(id)
            elif isinstance(id, bytes):
                id = ULID.from_bytes(id)
        except ValueError:
            return None

        return super().get(db, id.bytes)

    def create(self, db: Session, *, obj_in: VideoCreate) -> ModelVideo:
        # TODO: check global id
        if obj_in.source is None or obj_in.source_id is None:
            global_id = obj_in.global_id
            data = base64.b64decode(global_id)
            data = json.loads(data)
            obj_in.source = data['source']
            obj_in.source_id = data['id']

        # Find existing video by source and source_id
        video = db.query(ModelVideo).filter(
            ModelVideo.source == obj_in.source,
            ModelVideo.source_id == obj_in.source_id).first()
        if video:
            return video

        id = ULID()
        db_obj = ModelVideo(
            id=id.bytes,
            title=obj_in.title,
            source=obj_in.source,
            source_id=obj_in.source_id,
            status='created',
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        celery_app.send_task('vserver.worker.get_video_info', args=[str(id)])

        return db_obj


video = Video(ModelVideo)
