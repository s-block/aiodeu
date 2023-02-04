import cProfile
from datetime import datetime
import tracemalloc

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
                    "6": {
                        "7": {
                            "8": {
                                "9": {
                                    "11": {
                                        "12": {
                                            "13": "Thirteen"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


def profile(f, *args, **kwargs):
    st = datetime.now()
    for x in range(100000):
        f(*args, **kwargs)
    print(datetime.now() - st)


def run():
    cProfile.run('profile(cget_field, "header.3.4.5.6.7.8.9.10.11.12.13", TEST_DATA)')
    cProfile.run('profile(get_field, "header.3.4.5.6.7.8.9.10.11.12.13", TEST_DATA)')
    print("--------------")
    tracemalloc.start()
    profile(cget_field, "header.3.4.5.6.7.8.9.10.11.12.13", TEST_DATA)
    ss = tracemalloc.take_snapshot()
    ts = ss.statistics("lineno")
    [print(s) for s in ts]
    print(tracemalloc.get_traced_memory())
    tracemalloc.reset_peak()
    profile(get_field, "header.3.4.5.6.7.8.9.10.11.12.13", TEST_DATA)
    ss = tracemalloc.take_snapshot()
    ts = ss.statistics("lineno")
    [print(s) for s in ts]
    print(tracemalloc.get_traced_memory())
    print("--------------")
    profile(cexplode_list, TEST_DATA["header"], "2")
    profile(explode_list, TEST_DATA["header"], "2")
    print("--------------")


if __name__ == "__main__":
    run()
