from io import BytesIO
import os
import sys

from avro.datafile import DataFileReader
from avro.io import DatumReader

sys.path.insert(0, os.getcwd())

from tests.fixtures import TEST_AVRO_BYTES


avro_bytes = BytesIO(TEST_AVRO_BYTES)

reader = DataFileReader(avro_bytes, DatumReader())
schema = reader.meta
print(schema)
