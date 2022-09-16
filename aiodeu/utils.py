import asyncio
import json
import os
from functools import wraps, partial


class BytesJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode("utf-8")
            except UnicodeDecodeError:
                return ""
        return super().default(obj)


def write_to_file(path: str, contents: str) -> str:
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(contents)
    return path


def async_wrap(func):
    @wraps(func)
    async def run_async(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run_async
