#!/usr/bin/env python
import argparse
import asyncio
import json
import os

try:
    from avro.datafile import DataFileReader
    from avro.io import DatumReader
except ImportError:
    print("You need to install the dev requirements")

from aiodeu.utils import BytesJsonEncoder


def read_avro(file_path):
    return DataFileReader(open(file_path, "rb"), DatumReader())


def get_path(path: str) -> str:
    return os.path.abspath(os.path.join(os.getcwd(), path))


async def avro_to_json(in_path: str, out_path: str = "") -> None:
    reader = read_avro(get_path(in_path))
    rows = [record for record in reader]
    print(json.dumps(rows, cls=BytesJsonEncoder))
    if out_path:
        with open(get_path(out_path), "+w") as f:
            f.write(json.dumps(rows, cls=BytesJsonEncoder))


async def print_avro_schema(in_path: str, out_path: str = "") -> None:
    reader = read_avro(get_path(in_path))
    schema = reader.meta
    print(json.dumps(schema))
    if out_path:
        with open(get_path(out_path), "+w") as f:
            f.write(json.dumps(schema))


async def run(args):
    if args.func == "avro_to_json":
        await avro_to_json(args.in_path, args.out_path)
    if args.func == "print_avro_schema":
        await print_avro_schema(args.in_path, args.out_path)
    else:
        print("Must specify one of 'avro_to_json' or 'print_avro_schema'")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("func", metavar="Function", type=str, nargs=1, help="Function to run",
                        choices=("avro_to_json", "print_avro_schema"))
    parser.add_argument("-i", "--in", dest="in_path", type=str, default="")
    parser.add_argument("-o", "--out", dest="out_path", type=str, default="")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args))
