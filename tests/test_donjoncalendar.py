from app.modules.donjon.calendar import ElderanCalendar
from app.modules.donjon.date import ElderanDate


def test_campaign_start(elderan_calendar, campaign_start_date):
    assert elderan_calendar.campaign_start == campaign_start_date
