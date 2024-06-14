import json
from typing import BinaryIO

import httpx


class RequestService:
    """ REST API request handler """

    __slots__ = "url", "body", "timeout", "method", "content_json", "status_code", "query", "exc", "file", "data", "client"

    SUCCESSFUL_RESPONSE = {
        "get": 200,
        "post": 201,
        "put": 202,
        "delete": 204,
    }

    def __init__(self, url: str, body: dict = None, query: dict = None, file: BinaryIO = None, data: dict = None,
                 timeout: int = 5):
        self.url: str = url
        self.body: dict = body
        self.query: dict = query
        self.timeout: int = timeout
        self.file: BinaryIO = file
        self.data: dict = data

        self.method = None
        self.content_json = {}
        self.status_code = None
        self.exc = None

        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.client.aclose()

    async def _try_response(self, method: str) -> bool:
        try:
            response = await self.client.request(method,
                                                 url=self.url,
                                                 json=self.body,
                                                 timeout=self.timeout,
                                                 params=self.query,
                                                 data=self.data,
                                                 files={'file': self.file} if self.file else None, )
        except Exception as E:
            self.exc = E
            return False
        self.status_code = response.status_code

        try:
            content_str = response.content.decode()
        except Exception as E:
            self.exc = E
            return False
        else:
            if content_str:
                try:
                    self.content_json = json.loads(content_str)
                except json.JSONDecodeError as E:
                    self.exc = E
                    return False

        return self.status_code == self.SUCCESSFUL_RESPONSE[method.lower()]

    async def get(self):
        return await self._try_response('GET')

    async def post(self):
        return await self._try_response('POST')

    async def put(self):
        return await self._try_response('PUT')

    async def delete(self):
        return await self._try_response('DELETE')
