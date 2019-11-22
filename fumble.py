import os
from app.modules.donjon.calendar import ElderanCalendar
from app.modules.donjon.date import ElderanDate

# Start date: Tirdas, 11th of First Seed, 3E2026
# Current date: Middas, 15th of Last Seed, 3E2026 (day 155 since camp. start)

def main():
    calendar = ElderanCalendar()

    # print('Tirdas, 11th of First Seed, 3E2026')
    start_date = ElderanDate(2026, 3, 11)
    print(f'{start_date.descr_format()}')

    # print('Middas, 15th of Last Seed, 3E2026')
    current_date = ElderanDate.today()
    print(f'{current_date.descr_format()}')

    # return  # temporary

    # calendar.campaign_start = '2026-3-11'
    # calendar.today = '2026-8-15'

    dates = [
        ElderanDate.from_iso_format('2026-7-22'),
        ElderanDate.from_iso_format('2025-7-22'),
        ElderanDate.from_iso_format('2027-7-22'),
        ElderanDate.from_iso_format('2026-3-11'),
        ElderanDate.from_iso_format('2026-7-20'),
    ]

    print(f'Today: {calendar.today}')
    print(f'Day of year: {calendar.day_of_year}')
    print(f'Days since calendar start: {calendar.days_since()}')
    print(f'Days since campaign start: {calendar.days_since(calendar.campaign_start)}')
    print(f'Days since {dates[1]}: {calendar.days_since(dates[1])}')
    days_before = calendar.day_of_year - calendar.days_since(calendar.campaign_start)
    print(f'Days before campaign start: {days_before}')
    print(f'Weekday (today): {calendar.weekday(calendar.today)}')
    print(f'Weekday ({dates[0]}): {calendar.weekday(dates[0])}')  # Sundas
    print(f'Weekday ({dates[1]}): {calendar.weekday(dates[1])}')  # No idea if this is correct
    print(f'Weekday ({dates[2]}): {calendar.weekday(dates[2])}')  # No idea if this is correct
    print(f'Weekday ({dates[3]}): {calendar.weekday(dates[3])}')  # Tirdas
    print(f'Notes (today): {calendar.get_notes(calendar.today)}')
    print(f'Notes ({dates[4]}): {calendar.get_notes(dates[4])}')
    print(f'Notes (month): {calendar.get_notes(year=2025, month=12)}')
    print(f'JSON (today): {calendar.to_json_day()}')
    print(f'JSON (month): {calendar.to_json_month()}')
    print(f'JSON (year): {calendar.to_json_year()}')


if __name__ == '__main__':
    main()
