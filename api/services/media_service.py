from typing import BinaryIO

from services.request import RequestService
from settings import settings


class MediaServiceURLs:

    @property
    def media_service(self):
        return settings.MEDIA_SERVICE_URL

    @property
    def images(self):
        return f'{self.media_service}/images/'

    def image(self, key):
        return f'{self.media_service}/images/{key}/'


class MediaService:

    def __init__(self):
        self.URL = MediaServiceURLs()

    async def get_urls(self, keys: list):
        async with RequestService(self.URL.images, query={"keys": keys}) as r:
            if await r.get():
                return True, r.content_json
            return False, r.content_json

    async def get_url(self, key: str):
        async with RequestService(self.URL.image(key)) as r:
            if await r.get():
                return True, r.content_json.get(key)
            return False, None

    async def upload_file(self, file: BinaryIO, key: str):
        async with RequestService(self.URL.images, file=file, data={"key": key}) as r:
            if await r.post():
                return True, r.content_json.get(key)
            return False, r.content_json.get(key)

    async def update_file(self, file: BinaryIO, key: str):
        async with RequestService(self.URL.images, file=file, data={"key": key}) as r:
            if await r.put():
                return True, r.content_json.get(key)
            return False, r.content_json.get(key)

    async def delete_file(self, key: str):
        async with RequestService(self.URL.image(key)) as r:
            if await r.delete():
                return True
            return False
