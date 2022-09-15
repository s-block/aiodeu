from datetime import datetime

from aiodeu.cetl import get_field as cget_field, explode_list as cexplode_list
from aiodeu.etl import get_field, explode_list

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
        ],
        "3": {
            "4": {
                "5": {
                    "6": "Six"
                }
            }
        }
    }
}


def profile(f, *args, **kwargs):
    st = datetime.now()
    for x in range(1000000):
        f(*args, **kwargs)
    print(datetime.now() - st)


def run():
    profile(cget_field, "header.3.4.5.6.7", TEST_DATA)
    profile(get_field, "header.3.4.5.6.7", TEST_DATA)
    print("--------------")
    profile(cexplode_list, TEST_DATA["header"], "2")
    profile(explode_list, TEST_DATA["header"], "2")
    print("--------------")


if __name__ == "__main__":
    run()
