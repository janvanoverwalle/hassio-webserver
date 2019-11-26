import pytest
from app.modules.donjon.calendar import ElderanCalendar
from app.modules.donjon.date import ElderanDate


def pytest_configure(config):
    ElderanDate._CFG_PATH = 'tests/data/elderan-calendar.json'


@pytest.fixture
def elderan_json():
    json_data = None
    with open('tests/data/elderan-calendar.json') as json_file:
        json_data = json.load(json_file)
    return json_data


@pytest.fixture
def elderan_calendar():
    return ElderanCalendar()


@pytest.fixture
def elderan_date_ordinal():
    return 735186


@pytest.fixture
def elderan_date_iso():
    return '2026-04-20'


@pytest.fixture
def elderan_date_tuple():
    return (2026, 4, 20)


@pytest.fixture
def elderan_date():
    return ElderanDate(2026, 4, 20)
