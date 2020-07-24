import os

from src import app_logic


def test_get_percentage_failed():
    app_logic.get_percentage_passed(subject="Math 3", year="2019-2020")
    pass
