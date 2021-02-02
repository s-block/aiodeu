import logging
import os
import ssl

import faust
from faust.serializers import codecs

from consumer.codecs import AvroJsonCodec
from consumer.config import Config
from consumer.utils import write_to_file

codecs.register('AvroJsonCodec', AvroJsonCodec())

logger = logging.getLogger(__name__)


app_kwargs = {
    "broker": Config.BROKER_LIST,
    "value_serializer": "AvroJsonCodec",
    "store": "memory://",
    "topic_replication_factor": 3,
    "topic_partitions": 12,
    "topic_allow_declare": False,
    "topic_disable_leader": True,
    "consumer_auto_offset_reset": "latest"
}


if Config.BROKER_CERT:
    cert = write_to_file(os.path.join(Config.BASE_DIR, "client.cert"), Config.BROKER_CERT)
    key = write_to_file(os.path.join(Config.BASE_DIR, "client.key"), Config.BROKER_KEY)
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    ssl_context.load_cert_chain(cert, keyfile=key)
    app_kwargs.update({
        "broker_credentials": ssl_context
    })


def create_app():
    new_app = faust.App(
        Config.APP_NAME,
        **app_kwargs
    )
    return new_app


app = create_app()
