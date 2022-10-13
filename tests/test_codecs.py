import json

import pytest

from aiodeu.codecs import AvroJsonCodec
from aiodeu.utils import BytesJsonEncoder


@pytest.mark.asyncio()
async def test_loads(registry_server, test_message_serializer, test_avro_data, test_client):
    serializer = AvroJsonCodec()
    serializer.message_serializer = test_message_serializer
    serializer.client = test_client
    schema_id = registry_server.schema_id
    for avro_data in test_avro_data:
        in_data = json.loads(json.dumps(avro_data, cls=BytesJsonEncoder))
        serialised = serializer._dumps(obj=in_data, schema_id=schema_id)
        out_data = serializer._loads(serialised)
        assert out_data == in_data
