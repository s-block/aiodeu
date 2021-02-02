import json
from unittest import mock

from consumer.codecs import AvroJsonCodec
from consumer.utils import BytesJsonEncoder


def test_loads(registry_server, test_message_serializer, test_avro_data, test_client):
    with mock.patch('consumer.codecs.message_serializer', test_message_serializer):
        with mock.patch('consumer.codecs.client', test_client):
            serializer = AvroJsonCodec()
            schema_id = registry_server.schema_id
            in_data = json.loads(json.dumps(test_avro_data, cls=BytesJsonEncoder))
            serialised = serializer._dumps(obj=in_data, schema_id=schema_id)
            out_data = serializer._loads(serialised)
            assert out_data == in_data
