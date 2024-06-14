from pathlib import Path

from fastapi import UploadFile, HTTPException


class FileExtensionValidator:
    message = 'Extension “{extension}” not allowed. Allowed extensions are {allowed_extensions}'

    def __init__(self, allowed_extensions=None, message=None):
        if allowed_extensions is not None:
            allowed_extensions = [allowed_extension.lower() for allowed_extension in allowed_extensions]
        self.allowed_extensions = allowed_extensions
        if message is not None:
            self.message = message

    def __call__(self, file: UploadFile):
        extension = Path(file.filename).suffix[1:].lower()
        if self.allowed_extensions is not None and extension not in self.allowed_extensions:
            detail = self.message.format(extension=extension, allowed_extensions=', '.join(self.allowed_extensions))
            raise HTTPException(400, detail=detail)


class MaxFileSizeMBValidator:
    def __init__(self, max_mb: int):
        self.max_mb = max_mb

    def __call__(self, file: UploadFile):
        if file.size / 1024 / 1024 > self.max_mb:
            message = f'Maximum file size exceeded'
            raise HTTPException(400, detail=message)
