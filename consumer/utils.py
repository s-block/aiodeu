import json
import os


class BytesJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode("utf-8")
            except UnicodeDecodeError:
                return ""
        return super().default(obj)


def write_to_file(path, contents):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(contents)
    return path
