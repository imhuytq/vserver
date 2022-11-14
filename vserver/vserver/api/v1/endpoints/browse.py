import base64
import json
from typing import Any
from urllib.parse import urlparse
from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup


api_router = APIRouter()
session = requests.Session()


@api_router.get('/xvideos')
async def browse_xvideos(url: str = '/') -> Any:
    """
    Browse xvideos.
    """
    url = urlparse(url)
    if url.scheme != 'https':
        url = url._replace(scheme='https')
    if url.netloc != 'xvideos.com':
        url = url._replace(netloc='xvideos.com')

    html_text = session.get(url.geturl()).text
    soup = BeautifulSoup(html_text, 'lxml')
    videos = []
    pagination = []

    for v in soup.select('#content > div.mozaique.cust-nb-cols > div[id^="video_"]'):
        title_element = v.select_one('div.thumb-under > p.title > a')
        img_element = v.select_one('img[id^="pic_"]')
        title = title_element.attrs['title']
        url = title_element.attrs['href']
        url = 'https://xvideos.com' + url
        thumbnail = img_element.attrs['data-src']
        quality_element = v.select_one('div.thumb-inside > div.thumb > a > span')
        quality = quality_element and quality_element.text
        duration_element = v.select_one('div.thumb-under > p.metadata span.duration')
        duration = duration_element and duration_element.text
        id = v.attrs['data-id']
        global_id = base64.b64encode(json.dumps({
            'source': 'xvideos',
            'id': id,
        }).encode('utf-8'))

        videos.append({
            'id': id,
            'global_id': global_id,
            'title': title,
            'url': url,
            'thumbnail': thumbnail,
            'quality': quality,
            'duration': duration,
        })

    pagination_element = soup.select_one('.pagination')

    if pagination_element:
        for p in pagination_element.select('ul > li'):
            text = p.text.strip()
            url = p.select_one('a').attrs['href']
            url = url != '#' and 'https://xvideos.com' + url or None

            pagination.append({
                'text': text,
                'disabled': url is None,
                'url': url,
            })

    return {
        'videos': videos,
        'pagination': pagination,
    }
