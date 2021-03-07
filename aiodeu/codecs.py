from typing import Any

from faust.serializers import codecs
from schema_registry.client import SchemaRegistryClient
from schema_registry.serializers import MessageSerializer

from aiodeu.config import Config
from aiodeu.utils import async_wrap

client = SchemaRegistryClient(Config.AVRO_SCHEMA_REGISTRY)

message_serializer = MessageSerializer(client)


class AvroJsonCodec(codecs.Codec):
    """Schema registry /schemas/ids/1263"""
    async def _dumps(self, obj: dict, schema_id: int = 1) -> bytes:
        """Not used in application but for testing sending avro binary to kafka"""
        async_get_by_id = async_wrap(client.get_by_id)
        avro_schema = await async_get_by_id(schema_id)
        async_encode_record_with_schema = async_wrap(message_serializer.encode_record_with_schema)
        return await async_encode_record_with_schema(subject=Config.TOPIC_NAME, avro_schema=avro_schema, record=obj)

    async def _loads(self, s: bytes) -> Any:
        """Load avro binary and return reader iterable"""
        async_decode_message = async_wrap(message_serializer.decode_message)
        return await async_decode_message(s)
