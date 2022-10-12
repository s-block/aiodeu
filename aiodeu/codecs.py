from typing import Any

from faust.serializers import codecs
from schema_registry.client import SchemaRegistryClient
from schema_registry.serializers import AvroMessageSerializer

from aiodeu.config import Config

client = SchemaRegistryClient(Config.AVRO_SCHEMA_REGISTRY)

message_serializer = AvroMessageSerializer(client)


class AvroJsonCodec(codecs.Codec):
    """Schema registry /schemas/ids/1263"""
    def _dumps(self, obj: dict, schema_id: int = 1) -> bytes:
        """Not used in application but for testing sending avro binary to kafka"""
        avro_schema = client.get_by_id(schema_id)
        return message_serializer.encode_record_with_schema(subject=Config.TOPIC_NAME, schema=avro_schema, record=obj)

    def _loads(self, s: bytes) -> Any:
        """Load avro binary and return reader iterable"""
        return message_serializer.decode_message(s)
