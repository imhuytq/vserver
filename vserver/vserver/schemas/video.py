import base64
import json
from typing import Any, Dict, Optional
from enum import Enum

from pydantic import validator, root_validator
from pydantic.dataclasses import dataclass
import ulid

from .base import Base, InDBBase


class VideoSource(str, Enum):
    xvideos = 'xvideos'


class VideoBase(Base):
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    source: Optional[VideoSource] = None
    source_id: Optional[str] = None


class VideoCreate(VideoBase):
    global_id: Optional[str] = None

    @root_validator()
    def check_a_or_b(cls, values):
        if ((values.get('source') is None) or (values.get('source_id') is None)) and (values.get("global_id") is None):
            raise ValueError('either a or b is required')
        return values


class VideoUpdate(VideoBase):
    pass


class VideoInDBBase(VideoBase, InDBBase):
    id: Optional[bytes] = None
    source_url: Optional[str] = None
    status: Optional[str] = None


class Video(VideoInDBBase):
    @validator('id', pre=True)
    def id_to_str(cls, v):
        if isinstance(v, bytes):
            return str(ulid.ULID.from_bytes(v))
        return v
