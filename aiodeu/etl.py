import csv
import io
from itertools import chain
from typing import Any, Union


def get_conditional_data(items: list, dot_path: str, values: Union[list, str, int]) -> Union[dict, None]:
    """
    Returns contitional data from within a dict

    :param items:
    :param dot_path:
    :param values:
    :return:
    """
    if not isinstance(values, list):
        values = [values]
    for item in items:
        item_value = get_field(dot_path, item)
        if item_value in values:
            return item
    return None


def get_field(dot_path: str, record: Any) -> Any:
    """
    Returns data in dict with dot path

    :param dot_path:
    :param record:
    :return:
    """
    field, *fields = dot_path.split(".")
    dp = ".".join(fields)
    if not field:
        if record is None:
            return ""
        return record
    if isinstance(record, dict):
        val = record.get(field)
        return get_field(dp, val)
    elif isinstance(record, list):
        if len(record):
            val = record[0].get(field)
            return get_field(dp, val)
        return [get_field(dp, val) for val in record]
    else:
        if record is None:
            return ""
        return record


def explode_lists(data: list, field: str) -> list:
    """
    Explode field within a dict of a list of dicts. Calls below function.

    :param data:
    :param field:
    :return:
    """
    return list(chain(*[explode_list(d, field) for d in data]))


def explode_list(data: dict, field: str, prefix: Union[str, None] = None) -> list:
    """
    Explode a dict in to a list of dicts on a particular field that is a nested list. This will duplicate top level
    fields.

    :param data:
    :param field:
    :param prefix:
    :return:
    """
    if prefix is None:
        prefix = f"{field}."
    data_list = []
    field_list = data[field]
    top_level_data = {key: value for key, value in data.items() if key != field}
    for row in field_list:
        d = {}
        d.update(top_level_data)
        d.update({f"{prefix}{key}": value for key, value in row.items()})
        data_list.append(d)
    return data_list


async def data_to_csv_string(data: list, fieldnames: list = []) -> str:
    """
    Convert response to csv string

    :param data:
    :param fieldnames:
    :return str:
    """
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames or data[0].keys(),
        quoting=csv.QUOTE_ALL
    )
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
