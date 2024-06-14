from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form

from crud.memes import MemesCRUD
from models.memes import MemeUpdate, MemeIn, Meme
from routes.validators import MaxFileSizeMBValidator, FileExtensionValidator
from services.media_service import MediaService
from settings import settings

router = APIRouter()


@router.get("/memes", response_model=list[Optional[Meme]])
async def read_memes(offset: int = 0, limit: int = 10, memes_crud: MemesCRUD = Depends()):
    memes = await memes_crud.read_all(offset=offset, limit=limit)
    memes_keys = [m.image_key for m in memes]
    if memes_keys:
        ms = MediaService()
        status, result = await ms.get_urls(memes_keys)
        if not status:
            raise HTTPException(status_code=500, detail="Internal error")
        for meme in memes:
            meme.image_url = result.get(meme.image_key)
    return memes


@router.get("/memes/{meme_id}", response_model=Meme)
async def read_meme(meme_id: int, memes_crud: MemesCRUD = Depends()):
    db_meme = await memes_crud.read_one_by_id(meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    ms = MediaService()
    status, result = await ms.get_url(db_meme.image_key)
    if not status:
        raise HTTPException(status_code=404, detail="Meme not found")
    db_meme.image_url = result
    return db_meme


@router.post("/memes",
             response_model=Meme,
             dependencies=[
                 Depends(MaxFileSizeMBValidator(max_mb=settings.ALLOWED_SIZE_MB)),
                 Depends(FileExtensionValidator(allowed_extensions=settings.ALLOWED_EXTENSIONS)),
             ]
             )
async def create_meme(title: str = Form(),
                      description: str = Form(),
                      file: UploadFile = File(),
                      memes_crud: MemesCRUD = Depends()):
    meme = MemeIn(title=title, description=description, image_key=f'{title}_{file.filename}')
    if await memes_crud.read_one_by_title(meme_title=meme.title):
        raise HTTPException(status_code=404, detail="Meme with such title already exsists")
    ms = MediaService()
    status, result = await ms.upload_file(file.file, meme.image_key)
    if not status:
        raise HTTPException(status_code=400, detail="Meme creation failed")
    meme = await memes_crud.create(meme)
    meme.image_url = result
    return meme


@router.put("/memes/{meme_id}",
            response_model=Meme,
            dependencies=[
                Depends(MaxFileSizeMBValidator(max_mb=settings.ALLOWED_SIZE_MB)),
                Depends(FileExtensionValidator(allowed_extensions=settings.ALLOWED_EXTENSIONS)),
            ]
            )
async def update_meme(meme_id: int,
                      title: str = Form(...),
                      description: str = Form(...),
                      file: UploadFile = File(...),
                      memes_crud: MemesCRUD = Depends()):
    meme = MemeUpdate(title=title, description=description)
    if not (db_meme := await memes_crud.read_one_by_id(meme_id=meme_id)):
        raise HTTPException(status_code=404, detail="Meme not found")
    ms = MediaService()
    status, result = await ms.update_file(file.file, db_meme.image_key)
    if not status:
        raise HTTPException(status_code=400, detail="Meme update failed")
    meme = await memes_crud.update(meme, meme_id)
    meme.image_url = result
    return meme


@router.delete("/memes/{meme_id}")
async def delete_meme(meme_id: int, memes_crud: MemesCRUD = Depends()):
    db_meme = await memes_crud.read_one_by_id(meme_id=meme_id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    ms = MediaService()
    status = await ms.delete_file(db_meme.image_key)
    if not status:
        raise HTTPException(status_code=404, detail="Meme deletion failed")
    await memes_crud.delete(meme_id)
    return
