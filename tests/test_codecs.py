import json
from unittest import mock

import pytest

from aiodeu.codecs import AvroJsonCodec
from aiodeu.utils import BytesJsonEncoder


@pytest.mark.asyncio()
async def test_loads(registry_server, test_message_serializer, test_avro_data, test_client):
    with mock.patch('aiodeu.codecs.message_serializer', test_message_serializer):
        with mock.patch('aiodeu.codecs.client', test_client):
            serializer = AvroJsonCodec()
            schema_id = registry_server.schema_id
            for avro_data in test_avro_data:
                in_data = json.loads(json.dumps(avro_data, cls=BytesJsonEncoder))
                serialised = serializer._dumps(obj=in_data, schema_id=schema_id)
                out_data = serializer._loads(serialised)
                assert out_data == in_data
