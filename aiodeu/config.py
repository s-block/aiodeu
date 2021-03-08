import os


class Config:
    DEBUG: bool = False
    APP_NAME: str = os.environ.get("APP_NAME", "app_consumer").rstrip()
    BASE_DIR: str = os.getcwd()
    TOPIC_NAME: str = os.environ.get("TOPIC_NAME", "test").rstrip()
    BROKER: str = os.environ.get("BROKER", "localhost:9092").rstrip()
    BROKER_LIST: list = [f"kafka://{b}" for b in os.environ.get("BROKER", "localhost:9092").split(",")]
    BROKER_HOSTS: list = os.environ.get("BROKER", "localhost:9092").split(",")
    ZOOKEEPER: list = os.environ.get("ZOOKEEPER", "localhost").split(",")
    BROKER_KEY: str = os.environ.get("BROKER_KEY", "")
    BROKER_CERT: str = os.environ.get("BROKER_CERT", "")
    BROKER_GROUP_ID: str = os.environ.get("BROKER_GROUP_ID", "").rstrip()
    AVRO_SCHEMA_REGISTRY: str = f'http://{os.environ.get("AVRO_SCHEMA_REGISTRY", "127.0.0.1:8080").rstrip()}'
    AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID", "").rstrip()
    AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY", "").rstrip()
    AWS_S3_BUCKET_NAME: str = os.environ.get("AWS_S3_BUCKET_NAME", "test").rstrip()
    KEY_PREFIX: str = os.environ.get("KEY_PREXIX", "test/").rstrip()
    AWS_S3_REGION: str = os.environ.get("AWS_S3_REGION", "eu-west-2").rstrip()
