from typing import Optional

from pydantic import BaseModel, ConfigDict


class MemeUpdate(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        'example': {
            "title": "some_name",
            "description": "some text",
        }
    })


class MemeIn(MemeUpdate):
    image_key: str

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        'example': {
            "name": "some_name",
            "description": "some text",
            'image_key': "some_key.jpg",
        }
    })


class Meme(MemeUpdate):
    id: int
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        'example': {
            "name": "some_name",
            "description": "some text",
            'image_key': "some_key.jpg",
            'id': 2,
            'image_url': "http://url.com/image",  # noqa
        }
    })
