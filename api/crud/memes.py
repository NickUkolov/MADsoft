from typing import Sequence

from sqlalchemy import select

from crud.common import CRUD
from db.tables import Meme
from models.memes import MemeUpdate, MemeIn


class MemesCRUD(CRUD):

    async def read_one_by_id(self, meme_id: int) -> Meme:
        result = await self.session.execute(select(Meme).where(Meme.id == meme_id).limit(1))
        return result.scalars().first()

    async def read_one_by_title(self, meme_title: str) -> Meme:
        result = await self.session.execute(select(Meme).where(Meme.title == meme_title).limit(1))
        return result.scalars().first()

    async def read_all(self, offset: int = 0, limit: int = 10) -> Sequence[Meme]:
        result = await self.session.execute(select(Meme).offset(offset).limit(limit))
        return result.scalars().all()

    async def create(self, meme: MemeIn):
        db_meme = Meme(**meme.model_dump())
        self.session.add(db_meme)
        await self.session.commit()
        await self.session.refresh(db_meme)
        return db_meme

    async def update(self, meme: MemeUpdate, meme_id: int):
        db_meme = await self.read_one_by_id(meme_id)
        for key, value in meme.model_dump().items():
            setattr(db_meme, key, value)
        await self.session.commit()
        await self.session.refresh(db_meme)
        return db_meme

    async def delete(self, meme_id: int):
        db_meme = await self.read_one_by_id(meme_id)
        await self.session.delete(db_meme)
        await self.session.commit()
