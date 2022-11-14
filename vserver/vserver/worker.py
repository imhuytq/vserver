import json
import os

from yt_dlp import YoutubeDL
from ulid import ULID

from vserver.db.session import SessionLocal
from vserver.core.celery_app import celery_app
from vserver.models.video import Video

db = SessionLocal()


@celery_app.task(acks_late=True)
def test_celery(url: str) -> str:
    paths = os.path.join(os.getcwd(), 'downloads')
    ydl_opts = {
        # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # 'outtmpl': '%(title)s.%(ext)s',
        # 'cachedir': False,
        # 'debug_printtraffic': True,
        # 'cookiefile': cookiepath,
        'paths': {
            'home': paths,
        },
        'outtmpl': '%(extractor)s/%(id)s.%(ext)s',
        'verbose': True,
        # 'quiet': True,
        # 'youtube_include_dash_manifest': True,
        # 'youtube_include_hls_manifest': True,
        # 'extractor_args': {
        #     'youtube': {
        #         'player_client': ['ios_embedded'],
        #     },
        # },
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, True)
        data = json.dumps(ydl.sanitize_info(info), indent=4)
        # write to file
        with open('data.json', 'w') as f:
            f.write(data)


@celery_app.task(acks_late=True)
def get_video_info(id: str) -> str:
    id_bin = ULID.from_str(id).bytes
    video = db.query(Video).filter(Video.id == id_bin).first()
    
    if video is None:
        return 'Video not found'

    video.status = 'crawling'
    db.add(video)
    db.commit()

    paths = os.path.join(os.getcwd(), 'downloads')
    ydl_opts = {
        # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # 'outtmpl': '%(title)s.%(ext)s',
        # 'cachedir': False,
        # 'debug_printtraffic': True,
        # 'cookiefile': cookiepath,
        'paths': {
            'home': paths,
        },
        'outtmpl': '%(extractor)s/%(id)s.%(ext)s',
        'verbose': True,
        # 'quiet': True,
        # 'youtube_include_dash_manifest': True,
        # 'youtube_include_hls_manifest': True,
        # 'extractor_args': {
        #     'youtube': {
        #         'player_client': ['ios_embedded'],
        #     },
        # },
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video.source_url, video.need_download)
            source_info = {
                'title': info.get('fulltitle'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
            }

            video.source_info = source_info
            video.status = 'crawled'
        except Exception as e:
            video.status = 'error'
            video.error = str(e)

        db.add(video)
        db.commit()

    return id
