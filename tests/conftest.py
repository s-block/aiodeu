import os
import json
import pytest
from schema_registry.client import schema
from schema_registry.serializers import MessageSerializer

from consumer.app import (
    app,
)
from consumer.config import Config

from tests.fixtures import (
    TEST_AVRO_DATA,
    NEW_AVRO_BYTES,
)
from tests.mock_schema_registry_client import MockSchemaRegistryClient
from tests.mock_server import ServerThread


@pytest.fixture()
def test_avro_bytes():
    return NEW_AVRO_BYTES


@pytest.fixture()
def test_avro_data():
    return TEST_AVRO_DATA


@pytest.fixture()
def test_app(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app


@pytest.fixture(scope='session')
def test_client():
    return MockSchemaRegistryClient()


@pytest.fixture(scope='session')
def test_message_serializer(test_client):
    return MessageSerializer(test_client)


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

        av_schema = schema.AvroSchema(json_data.get('schema'))
        self.schema_id = self.client.register('landing-1-value', av_schema)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.shutdown()


@pytest.fixture()
def registry_server(test_message_serializer, test_client):
    with RegistryServerWrapper(test_message_serializer, test_client) as sr:
        yield sr
