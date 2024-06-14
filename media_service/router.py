from typing import List

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query, Path, status

from s3_utils import minio_client

router = APIRouter(prefix="/images")


@router.get("/",
            response_model=dict,
            status_code=status.HTTP_200_OK,
            responses={
                200: {
                    "description": "URLs successfully get, failed to get urls are null",
                    "content": {
                        "application/json": {
                            "example": {
                                "key1": "url1",
                                "key2": "url2"
                            }
                        }
                    }
                }
            }
            )
def get_presigned_urls(keys: List[str] = Query()):
    return minio_client.generate_presigned_urls(keys)


@router.get("/{key}/",
            response_model=dict,
            status_code=status.HTTP_200_OK,
            responses={
                200: {
                    "description": "URL successfully get",
                    "content": {
                        "application/json": {
                            "example": {
                                "key1": "url1"
                            }
                        }
                    }
                },
                400: {"description": "Failed to get url"}
            }
            )
def get_presigned_url(key: str = Path()):
    url = minio_client.generate_presigned_url(key)
    if not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not generate presigned URL")
    return {key: url}


@router.post("/",
             response_model=dict,
             status_code=status.HTTP_201_CREATED,
             responses={
                 201: {
                     "description": "File succsessfuly uploaded, url in response",
                     "content": {
                         "application/json": {
                             "example": {
                                 "key1": "url1"
                             }
                         }
                     }
                 },
                 400: {"description": "Object already exists"},
                 500: {"description": "Upload failed"}
             }
             )
def upload_file(file: UploadFile = File(),
                key: str = Form()):
    if minio_client.object_exists(key):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object already exists")
    if not minio_client.upload_file(file.file, key):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Upload failed")
    url = minio_client.generate_presigned_url(key)
    return {key: url}


@router.put("/",
            response_model=dict,
            status_code=status.HTTP_202_ACCEPTED,
            responses={
                202: {
                    "description": "File succsessfuly uploaded, url in response",
                    "content": {
                        "application/json": {
                            "example": {
                                "key1": "url1"
                            }
                        }
                    }
                },
                400: {"description": "Object does not exist"},
                500: {"description": "Upload failed"}
            }
            )
def update_file(file: UploadFile = File(),
                key: str = Form()):
    if not minio_client.object_exists(key):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object does not exist")
    if not minio_client.upload_file(file.file, key):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Upload failed")
    url = minio_client.generate_presigned_url(key)
    return {key: url}


@router.delete("/{key}/",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   204: {
                       "description": "File succsessfuly deleted",
                       "content": {
                           "application/json": {
                               "example": None
                           }
                       }
                   },
                   404: {"description": "Object does not exist or failed to delete"}
               }
               )
def delete_file(key: str = Path()):
    if not minio_client.delete_file(key):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object does not exist or failed to delete")
