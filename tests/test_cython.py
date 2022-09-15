import pytest

from aiodeu.cetl import get_field, get_conditional_data, explode_list


TEST_DATA = {
    "header": {
        "1": "One",
        "2": [
            {
                "f": "Three",
                "a": "Five"
            },
            {
                "f": "Four",
                "a": "Six"
            }
        ]
    }
}


@pytest.mark.parametrize("test_input,expected", [
    ("header.1", "One"),
    ("header.1.4", "One"),
    ("header.4", "")
])
def test_get_field(test_input, expected):
    assert get_field(test_input, TEST_DATA) == expected


def test_get_conditional_data():
    items = get_field("header.2", TEST_DATA)
    assert get_conditional_data(items, "f", "Four") == {'a': 'Six', 'f': 'Four'}


def test_explode_list():
    assert explode_list(TEST_DATA["header"], "2") == [
        {'1': 'One', '2.f': 'Three', '2.a': 'Five'},
        {'1': 'One', '2.f': 'Four', '2.a': 'Six'}
    ]
