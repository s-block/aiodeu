import io
import logging
import tempfile
from typing import Union

import boto3
from botocore.exceptions import ClientError

from aiodeu.config import Config
from aiodeu.utils import async_wrap

logger = logging.getLogger(__name__)


class StorageException(Exception):
    """Exception raised when file read errors"""
    pass


class S3Transport:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, region=Config.AWS_S3_REGION, sse="aws:kms"):
        self.resource = boto3.resource(
            "s3",
            region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket = self.resource.Bucket(bucket_name)
        self.sse = sse

    async def write(self, file_contents: Union[str, io.BytesIO], key: str) -> None:
        logger.info(f"Sending file to s3: {key}")
        if isinstance(file_contents, str):
            bytes_data = io.BytesIO()
            bytes_data.write(file_contents.encode("utf-8"))
        elif isinstance(file_contents, io.BytesIO):
            bytes_data = file_contents
        else:
            raise Exception("file_contents must be str or io.BytesIO")
        bytes_data.seek(0)
        upload_fileobj = async_wrap(self.bucket.upload_fileobj)
        await upload_fileobj(
            bytes_data, key,
            ExtraArgs={"ServerSideEncryption": self.sse}
        )

    async def read(self, file_path: str) -> Union[str, bytes]:
        """Returns file contents"""
        with tempfile.NamedTemporaryFile("w+b") as file_obj:
            try:
                download_file = async_wrap(self.bucket.download_file)
                await download_file(
                    file_path,
                    file_obj.name
                )
            except ClientError:
                raise StorageException(f"Can't download file: {file_path}")

            try:
                with open(file_obj.name, "r") as contents:
                    return contents.read()
            except UnicodeDecodeError:
                with open(file_obj.name, "rb") as contents:
                    return contents.read()
