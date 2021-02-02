import io
import json
import logging
import tempfile

import boto3
from botocore.exceptions import ClientError

from consumer.config import Config
from consumer.utils import BytesJsonEncoder

logger = logging.getLogger(__name__)


class StorageException(Exception):
    """Exception raised when file read errors"""
    pass


class S3Transport:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, region=Config.AWS_S3_REGION, sse='aws:kms'):
        self.resource = boto3.resource(
            "s3",
            region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket = self.resource.Bucket(bucket_name)
        self.sse = sse

    def write(self, file_contents, key):
        logger.info(f"Sending file to s3: {key}")
        bytes_data = io.BytesIO()
        bytes_data.write(file_contents.encode("utf-8"))
        bytes_data.seek(0)
        self.bucket.upload_fileobj(
            bytes_data, key,
            ExtraArgs={'ServerSideEncryption': self.sse}
        )

    def read(self, file_path):
        """Returns file contents"""
        with tempfile.NamedTemporaryFile('w+b') as file_obj:
            try:
                self.bucket.download_file(
                    file_path,
                    file_obj.name
                )
            except ClientError:
                raise StorageException('Can\'t download file: %s' % file_path)

            try:
                with open(file_obj.name, 'r') as contents:
                    return contents.read()
            except UnicodeDecodeError:
                with open(file_obj.name, 'rb') as contents:
                    return contents.read()


def record_to_json(record):
    return json.dumps(
        record, cls=BytesJsonEncoder
    ).replace(': "null",', ": null,") \
        .replace(': "true",', ": true,") \
        .replace(': "false",', ": false,") \
        .replace(': "Yes",', ": true,") \
        .replace(': "No",', ": false,")
