from app.modules.donjon.date import ElderanDate


def assert_date(date, tuple_date):
    if not tuple_date:
        assert False, f'no data given to compare'
    assert date.year == tuple_date[0], 'year mismatch'
    if len(tuple_date) > 1:
        assert date.month == tuple_date[1], 'month mismatch'
    if len(tuple_date) > 2:
        assert date.day == tuple_date[2], 'day mismatch'


def test_from_ordinal():
    date = ElderanDate.from_ordinal(735186)
    assert_date(date, (2026, 4, 20))


def test_from_iso_format():
    date = ElderanDate.from_iso_format('2026-04-20')
    print(date.to_ordinal())
    assert_date(date, (2026, 4, 20))


def test_today():
    date = ElderanDate.today()
    assert_date(date, (2026, 4, 20))


def test_iso_format():
    date = ElderanDate(2026, 4, 20)
    assert date.iso_format() == '2026-04-20'


def test_description_format():
    date = ElderanDate(2026, 4, 20)
    assert date.descr_format() == 'Loredas, 20th of Rain\'s Hand, 3E2026'

def test_properties():
    date = ElderanDate(2026, 4, 20)
    assert_date(date, (2026, 4, 20))

def test_to_ordinal():
    date = ElderanDate(2026, 4, 20)
    assert date.to_ordinal() == 735186

def test_replace():
    date = ElderanDate(2026, 4, 20)
    new_date = date.replace(month=5, day=21)
    assert_date(new_date, (2026, 5, 21))
