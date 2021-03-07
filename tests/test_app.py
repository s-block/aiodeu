import json

from fastavro import reader
import pytest


@pytest.mark.asyncio()
async def test_app(test_agent, test_avro_data, test_avro_bytes, s3_transport):
    async with test_agent.test_context() as agent:
        await agent.put(reader(test_avro_bytes))
        key = "test.json"
        s3_bucket = s3_transport.bucket
        assert [s.key for s in s3_bucket.objects.all()] == [key]
        assert json.loads(await s3_transport.read(key)) == test_avro_data
