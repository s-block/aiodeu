# Kafka consumer

## Setup
```bash
pyenv install 3.9.0
pyenv virtualenv 3.9.0 aiodeu
pyenv shell aiodeu
pip install -r requirements.txt
poetry install
```

## Test
```bash
pytest
```


### Run Kafka
https://kafka.apache.org/quickstart

From Docker:
```bash
docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=`docker-machine ip \`docker-machine active\`` --env ADVERTISED_PORT=9092 spotify/kafka
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' {CONTAINER_NAME}
/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --create --replication-factor 1 --partitions 1 --topic {{topic}} --zookeeper localhost:2181
```

Locally:
https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273
```bash
brew cask install java
brew install kafka
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties
```

Create topic:
```bash
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic {{topic}}
```

List topics:
```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Delete topic:
```bash
kafka-topics --zookeeper localhost:2181 --delete --topic {{topic}}
```

### Faust Consumer
Faust consumer setup with certs

Extract certs from .jks file
https://serverfault.com/questions/715827/how-to-generate-key-and-crt-file-from-jks-file-for-httpd-apache-server

```bash
keytool -importkeystore -srckeystore mycert.jks -destkeystore keystore.p12 -deststoretype PKCS12
openssl pkcs12 -in keystore.p12 -nokeys -out cert.crt
openssl pkcs12 -in keystore.p12 -nocerts -nodes -out key.key
```

```python
# app/agents.py
import logging

from aiodeu.app import create_app
from aiodeu.config import Config

logger = logging.getLogger(__name__)

app = create_app(Config)

topic = app.topic(Config.TOPIC_NAME)


@app.agent(topic)
async def etl(stream):
    logger.info("Message received")
    async for message in stream:
        for record in message:
            logger.info("Record per message")
```

```dockerfile
# Dockerfile
FROM python:3.9.2-slim-buster

ARG ENV_TYPE=base

RUN adduser -D -H 1000

RUN mkdir /faust
WORKDIR /faust

COPY requirements requirements
RUN pip install -r requirements/$ENV_TYPE.txt

COPY app app
COPY tests tests

RUN chown -R 1000 /faust

USER 1000

CMD [ "faust", "-A", "app.agents", "worker", "-l", "info" ]
```
