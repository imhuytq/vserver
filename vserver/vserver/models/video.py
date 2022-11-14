from sqlalchemy import Index, Column, String, Enum, LargeBinary, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from yt_dlp import YoutubeDL

from .base import Base


class Video(Base):
    id = Column(LargeBinary(16), primary_key=True)
    _title = Column('title', String)
    source = Column(String)
    source_id = Column(String)
    source_info = Column(JSON)
    download_status = Column(
        Enum(
            'pending', 'downloading', 'done', 'failed',
            name='video_download_status',
        ),
        index=True,
        nullable=True,
    )
    status = Column(
        Enum(
            'created', 'crawling', 'crawled', 'error',
            name='video_status',
        ),
        index=True,
        nullable=False,
    )
    error = Column(String)

    __table_args__ = (
        Index('ix_video_source', 'source', 'source_id', unique=True),
    )

    @hybrid_property
    def title(self):
        return self._title or self.source_info.get('title')

    @title.setter
    def title(self, value):
        self._title = value

    @hybrid_property
    def thumbnail(self):
        return self.source_info.get('thumbnail')

    @hybrid_property
    def source_url(self):
        if self.source == 'xvideos':
            return f'https://www.xvideos.com/video{self.source_id}/_'
        return None

    @hybrid_property
    def need_download(self) -> bool:
        return self.source != 'xvideos'

    @hybrid_property
    def urls(self):
        if not self.need_download:
            ydl_opts = {
                'quiet': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.source_url, False)
                formats = info.get('formats', [])

            return list(map(
                lambda f: {
                    'url': f['url'],
                    'format_id': f['format_id'],
                    'resolution': f['resolution'],
                },
                formats,
            ))

        return []
