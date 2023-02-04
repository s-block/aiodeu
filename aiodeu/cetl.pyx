from itertools import chain


cpdef object get_field(str dot_path, object record):
    """
    Returns data in dict with dot path

    :param dot_path:
    :param record:
    :return:
    """
    cdef str field
    cdef list fields
    field, *fields = dot_path.split(".")
    cdef str dp = ".".join(fields)
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


cpdef object get_conditional_data(list items, str dot_path, object values):
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


cpdef list explode_lists(list data, str field):
    """
    Explode field within a dict of a list of dicts. Calls below function.

    :param data:
    :param field:
    :return:
    """
    return list(chain(*[explode_list(d, field) for d in data]))


cpdef list explode_list(dict data, str field, str prefix = None):
    """
    Explode a dict in to a list of dicts on a particular field that is a nested list. This will duplicate top level
    fields.

    :param data:
    :param field:
    :param prefix:
    :return:
    """
    if prefix is None:
        prefix = "%s." % field
    cdef list data_list = []
    cdef list field_list = data[field]
    cdef dict top_level_data = {key: value for key, value in data.items() if key != field}
    cdef dict d
    for row in field_list:
        d = {}
        d.update(top_level_data)
        d.update({f"{prefix}{key}": value for key, value in row.items()})
        data_list.append(d)
    return data_list
