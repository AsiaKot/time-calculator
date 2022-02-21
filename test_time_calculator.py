import unittest
from parameterized import parameterized
from datetime import datetime

from time_calculator import TimeCalc


class TestTimeCalc(unittest.TestCase):
    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 00, 1), "za minutę"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 00, 2), "za 2 minuty"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 00, 3), "za 3 minuty"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 00, 5), "za 5 minut"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 00, 17), "za 17 minut"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 00, 22), "za 22 minuty"),
        ])
    def test_if_event_today_should_return_result_in_minutes(self, reference_date, event_datetime, result):
        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 1, 00), "za godzinę"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 2, 00), "za 2 godziny"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 3, 00), "za 3 godziny"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 5, 00), "za 5 godzin"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 17, 00), "za 17 godzin"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 22, 00), "za 22 godziny"),
        ])
    def test_if_event_today_should_return_result_in_hours(self, reference_date, event_datetime, result):
        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 1, 10), "za godzinę i 10 minut"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 2, 4), "za 2 godziny i 4 minuty"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 3, 20), "za 3 godziny i 20 minut"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 5, 2), "za 5 godzin i 2 minuty"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 17, 52), "za 17 godzin i 52 minuty"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 1, 22, 1), "za 22 godziny i minutę"),
    ])
    def test_if_event_today_should_return_result_in_hours_and_minutes(self, reference_date, event_datetime, result):
        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 2, 00, 00), "jutro o 00:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 2, 10, 10), "jutro o 10:10"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 2, 17, 00), "jutro o 17:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 2, 23, 59), "jutro o 23:59"),
    ])
    def test_if_event_2morrow_should_return_result_as_tomorrow_at_time(self, reference_date, event_datetime, result):
        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 3, 00, 00), "pojutrze o 00:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 3, 10, 10), "pojutrze o 10:10"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 3, 17, 00), "pojutrze o 17:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 3, 23, 59), "pojutrze o 23:59"),
    ])
    def test_if_event_dayafter2morrow_should_return_result_as_day_after_tomorrow_at_time(
            self, reference_date, event_datetime, result):

        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 4, 00, 00), "we wtorek o 00:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 5, 10, 10), "w środę o 10:10"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 6, 17, 00), "w czwartek o 17:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 7, 23, 59), "w piątek o 23:59"),
    ])
    def test_if_event_this_week_should_return_result_as_weekday_at_time(
            self, reference_date, event_datetime, result):

        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 8, 00, 00), "w przyszłą sobotę o 00:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 9, 10, 10), "w przyszłą niedzielę o 10:10"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 10, 17, 00), "w przyszły poniedziałek o 17:00"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 14, 23, 59), "w przyszły piątek o 23:59"),
    ])
    def test_if_event_next_week_should_return_result_as_next_weekday_at_time(
            self, reference_date, event_datetime, result):

        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 15, 00, 00), "za 14 dni"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 20, 00, 1), "za 19 dni i minutę"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 28, 11, 00), "za 27 dni i 11 godzin"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 30, 23, 59), "za 29 dni, 23 godziny i 59 minut"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 1, 31, 00, 21), "za 30 dni i 21 minut")
    ])
    def test_if_event_within_month_should_return_result_in_days_hours_and_minutes(
            self, reference_date, event_datetime, result):

        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 2, 1, 00, 00), "za miesiąc"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 5, 28, 11, 00), "za 4 miesiące i 27 dni"),
        (datetime(2022, 1, 1, 00, 00), datetime(2022, 12, 31, 23, 59), "za 11 miesięcy i 30 dni"),
    ])
    def test_if_event_within_year_should_return_result_in_months_and_days(
            self, reference_date, event_datetime, result):

        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)

    @parameterized.expand([
        (datetime(2022, 1, 1, 00, 00), datetime(2023, 1, 1, 00, 00), "za rok"),
        (datetime(2022, 1, 1, 00, 00), datetime(2024, 2, 1, 00, 00), "za 2 lata i miesiąc"),
        (datetime(2022, 1, 1, 00, 00), datetime(2027, 5, 28, 11, 00), "za 5 lat, 4 miesiące i 27 dni"),
        (datetime(2022, 1, 1, 00, 00), datetime(2032, 12, 31, 23, 59), "za 10 lat, 11 miesięcy i 30 dni")
    ])
    def test_if_event_next_years_should_return_result_in_years_months_and_days(
            self, reference_date, event_datetime, result):

        when_is_event = TimeCalc(event_datetime, reference_date).show_info()
        self.assertEqual(when_is_event, result)
