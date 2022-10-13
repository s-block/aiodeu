import logging
import os
import ssl
from typing import Type

import faust
from faust.serializers import codecs

from aiodeu.codecs import AvroJsonCodec
from aiodeu.config import Config
from aiodeu.utils import write_to_file

logger = logging.getLogger(__name__)


def create_app(config: Type[Config], faust_app_kwargs: dict = {}) -> faust.App:
    app_kwargs = {
        "broker": config.BROKER_LIST,
        "value_serializer": "AvroJsonCodec",
        "store": "memory://",
        "topic_replication_factor": 3,
        "topic_partitions": 12,
        "topic_allow_declare": False,
        "topic_disable_leader": True,
        "consumer_auto_offset_reset": "earliest",
        # "stream_wait_empty": False
    }
    cert_verify = faust_app_kwargs.pop("cert_verify", True)
    app_kwargs.update(faust_app_kwargs)
    codecs.register('AvroJsonCodec', AvroJsonCodec(config=config))

    if config.BROKER_CERT:
        cert = write_to_file(os.path.join(config.BASE_DIR, "client.cert"), config.BROKER_CERT)
        key = write_to_file(os.path.join(config.BASE_DIR, "client.key"), config.BROKER_KEY)
        if cert_verify:
            ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        else:
            ssl_context = ssl._create_unverified_context(purpose=ssl.Purpose.SERVER_AUTH)
        ssl_context.load_cert_chain(cert, keyfile=key)
        ssl_context.load_cert_chain(cert, keyfile=key)
        app_kwargs.update({
            "broker_credentials": ssl_context
        })

    new_app = faust.App(
        config.APP_NAME,
        **app_kwargs
    )
    return new_app
