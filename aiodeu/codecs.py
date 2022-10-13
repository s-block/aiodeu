from typing import Any, Type

from faust.serializers import codecs
from schema_registry.client import SchemaRegistryClient
from schema_registry.serializers import AvroMessageSerializer

from aiodeu.config import Config


class AvroJsonCodec(codecs.Codec):
    def __init__(self, *args, config: Type[Config] = Config, **kwargs: Any) -> None:
        self.config = config
        self.client = SchemaRegistryClient(self.config.AVRO_SCHEMA_REGISTRY)
        self.message_serializer = AvroMessageSerializer(self.client)
        super().__init__(*args, **kwargs)

    """Schema registry /schemas/ids/1263"""
    def _dumps(self, obj: dict, schema_id: int = 1) -> bytes:
        """Not used in application but for testing sending avro binary to kafka"""
        avro_schema = self.client.get_by_id(schema_id)
        return self.message_serializer.encode_record_with_schema(
            subject=self.config.TOPIC_NAME,
            schema=avro_schema,
            record=obj
        )

    def _loads(self, s: bytes) -> Any:
        """Load avro binary and return reader iterable"""
        return self.message_serializer.decode_message(s)
