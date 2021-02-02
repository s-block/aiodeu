"""
Example app - app.agents
===========

import logging

from consumer.app import app
from consumer.config import Config

logger = logging.getLogger(__name__)


topic = app.topic(Config.TOPIC_NAME)


@app.agent(topic)
async def etl(message):
    logger.info("Message received")
    async for record in message:
        logger.info("Record per message")
"""

try:
    from app.agents import app  # noqa
except ImportError:
    from consumer.app import app  # noqa
