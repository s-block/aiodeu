import json
import os
from unittest import mock

import boto3
from moto import mock_s3
import pytest
from schema_registry.client import schema
from schema_registry.serializers import AvroMessageSerializer

from aiodeu.app import (
    create_app,
)
from aiodeu.config import Config
from aiodeu.s3 import S3Transport

from tests.mock_schema_registry_client import MockSchemaRegistryClient
from tests.mock_server import ServerThread


@pytest.fixture()
def test_avro_bytes():
    with open(os.path.join(os.path.dirname(__file__), 'data/test.avro'), 'rb') as avro_file:
        yield avro_file


@pytest.fixture()
def test_avro_data():
    with open(os.path.join(os.path.dirname(__file__), 'data/test.jsonl'), 'r') as jsonl_file:
        data = []
        for line in jsonl_file.readlines():
            data.append(json.loads(line))
        return data


@pytest.fixture(scope='session', autouse=True)
def s3_resource():
    with mock_s3():
        s3 = boto3.resource('s3', region_name="eu-west-2")
        yield s3


@pytest.fixture(scope='session', autouse=True)
def s3_transport(s3_resource):
    location = {'LocationConstraint': "eu-west-2"}
    s3_bucket = s3_resource.create_bucket(Bucket=Config.AWS_S3_BUCKET_NAME, CreateBucketConfiguration=location)
    s3_transport = S3Transport(
        Config.AWS_ACCESS_KEY_ID,
        Config.AWS_SECRET_ACCESS_KEY,
        s3_bucket.name
    )
    yield s3_transport


@pytest.fixture(scope='session')
def test_client():
    return MockSchemaRegistryClient()


@pytest.fixture(scope='session')
def test_message_serializer(test_client):
    return AvroMessageSerializer(test_client)


class RegistryServerWrapper:
    def __init__(self, message_serializer=test_message_serializer, client=test_client):
        protocol, host, port = Config.AVRO_SCHEMA_REGISTRY.split(":")
        self.port = int(port)
        self.schema_id = None
        self.message_serializer = message_serializer
        self.client = client

    def __enter__(self):
        self.server = ServerThread(self.port)
        self.server.start()

        with open(os.path.join(os.path.dirname(__file__), 'data/test.avsc'), 'r') as json_string:
            json_data = json.load(json_string)

        av_schema = schema.AvroSchema(json_data)
        self.schema_id = self.client.register('test', av_schema)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.shutdown()


@pytest.fixture()
def registry_server(test_message_serializer, test_client):
    with RegistryServerWrapper(test_message_serializer, test_client) as sr:
        yield sr


@pytest.fixture()
def test_app(event_loop, test_message_serializer, test_client):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    with mock.patch('aiodeu.codecs.message_serializer', test_message_serializer):
        with mock.patch('aiodeu.codecs.client', test_client):
            app = create_app(Config)
            app.finalize()
            app.conf.store = 'memory://'
            app.flow_control.resume()
            yield app


@pytest.fixture()
def test_agent(test_app, s3_transport):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    topic = test_app.topic(Config.TOPIC_NAME, partitions=12)

    @test_app.agent(topic)
    async def agent(stream):
        data = []
        async for reader in stream:
            for record in reader:
                data.append(record)
            yield await s3_transport.write(json.dumps(data), "test.json")
    return agent
