import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from settings import settings


class MinioClient:

    def __init__(self, endpoint_url: str = settings.MINIO_URI, access_key: str = settings.MINIO_ROOT_USER,
                 secret_key: str = settings.MINIO_ROOT_PASSWORD, bucket_name=settings.MINIO_BUCKET):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = bucket_name

        if not self._check_bucket_exists():
            self._create_bucket()

    def _check_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError:
            return False

    def _create_bucket(self):
        self.s3_client.create_bucket(Bucket=self.bucket_name)

    def object_exists(self, object_key):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except ClientError:
            return False

    def generate_presigned_url(self, object_key, expiration=settings.MINIO_URL_TTL):
        exists = self.object_exists(object_key)
        if not exists:
            return None
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            return url
        except Exception:
            return None

    def generate_presigned_urls(self, object_keys, expiration=settings.MINIO_URL_TTL):
        presigned_urls = {}

        for key in object_keys:
            exists = self.object_exists(key)
            if not exists:
                presigned_urls[key] = None
            url = self.generate_presigned_url(key, expiration)
            if url:
                presigned_urls[key] = url
        return presigned_urls

    def upload_file(self, file, object_key):
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, object_key)
            return True
        except Exception:
            return False

    def delete_file(self, object_key) -> bool:
        exists = self.object_exists(object_key)
        if not exists:
            return False
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except Exception:
            return False


minio_client = MinioClient()
