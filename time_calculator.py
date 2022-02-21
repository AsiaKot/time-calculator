from datetime import datetime, timedelta


class TimeCalc:
    def __init__(self, event_datetime, reference_datetime=datetime.now()):
        self.event_datetime = event_datetime
        self.reference_datetime = reference_datetime

    def time_between(self):
        return self.event_datetime - self.reference_datetime

    def _calc_years_months_days_between(self):
        event_year = self.event_datetime.year
        reference_year = self.reference_datetime.year
        event_month = self.event_datetime.month
        reference_month = self.reference_datetime.month
        event_day = self.event_datetime.day
        reference_day = self.reference_datetime.day

        if event_year >= reference_year:
            if event_month >= reference_month:
                return TimeCalc._events_month_after_reference_month(
                    self.reference_datetime,
                    event_year,
                    reference_year,
                    event_month,
                    reference_month,
                    event_day,
                    reference_day,
                )
            return TimeCalc._events_month_before_reference_month(
                self.reference_datetime,
                event_year,
                reference_year,
                event_month,
                reference_month,
                event_day,
                reference_day,
            )

    @staticmethod
    def _events_month_after_reference_month(
        reference_datetime,
        event_year,
        reference_year,
        event_month,
        reference_month,
        event_day,
        reference_day,
    ):
        if event_day >= reference_day:
            years_between = event_year - reference_year
            months_between = event_month - reference_month
            days_between = event_day - reference_day
            return years_between, months_between, days_between

        years_between = event_year - reference_year
        months_between = event_month - reference_month - 1
        days_between = event_day + (
            TimeCalc.days_in_month(reference_datetime) - reference_day
        )
        return years_between, months_between, days_between

    @staticmethod
    def _events_month_before_reference_month(
        reference_datetime,
        event_year,
        reference_year,
        event_month,
        reference_month,
        event_day,
        reference_day,
    ):
        if event_day >= reference_day:
            years_between = event_year - reference_year - 1
            months_between = event_month + (12 - reference_month)
            days_between = event_day - reference_day
            return years_between, months_between, days_between

        years_between = event_year - reference_year - 1
        months_between = event_month + (12 - reference_month) - 1
        days_between = (
            event_day + (TimeCalc.days_in_month(reference_datetime) - reference_day) + 2
        )
        return years_between, months_between, days_between

    def _if_2omorrow(self):
        return self.time_between() / timedelta(minutes=1) <= 2879 and TimeCalc.weekday(
            self.event_datetime
        ) != TimeCalc.weekday(self.reference_datetime)

    def _if_day_after_2omorrow(self):
        return 1441 <= self.time_between() / timedelta(minutes=1) <= 4319

    def _if_this_week(self):
        return 4320 <= self.time_between() / timedelta(minutes=1) <= 10079

    def _if_next_week(self):
        return 10080 <= self.time_between() / timedelta(minutes=1) <= 20159

    def _return_years_between(self):
        years_between = self._calc_years_months_days_between()[0]
        if years_between == 0:
            return None
        if years_between == 1:
            return "rok"
        if years_between in range(2, 5):
            return f"{years_between} lata"
        return f"{years_between} lat"

    def _return_months_between(self):
        months_between = self._calc_years_months_days_between()[1]
        if months_between == 0:
            return None
        if months_between == 1:
            return "miesiąc"
        if months_between in range(2, 5):
            return f"{months_between} miesiące"
        return f"{months_between} miesięcy"

    def _return_days_between(self):
        days_between = self._calc_years_months_days_between()[2]
        if days_between == 0:
            return None
        if days_between == 1:
            return f"{days_between} dzień"
        return f"{days_between} dni"

    def _return_hours_between(self):
        hours_between = int(
            self.time_between() % timedelta(minutes=1440) / timedelta(minutes=60)
        )
        if hours_between == 0:
            return None
        if hours_between == 1:
            return "godzinę"
        if TimeCalc._last_num_is_2_3_4(hours_between):
            ending = "y"
        else:
            ending = ""
        return f"{hours_between} godzin{ending}"

    def _return_minutes_between(self):
        minutes_between = int(
            self.time_between() % timedelta(minutes=60) / timedelta(minutes=1)
        )
        if minutes_between == 0:
            return None
        if minutes_between == 1:
            return "minutę"
        if TimeCalc._last_num_is_2_3_4(minutes_between):
            ending = "y"
        else:
            ending = ""
        return f"{minutes_between} minut{ending}"

    def _info_tomorrow_at_time(self):
        return f"jutro o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"

    def _info_day_after_2morrow_at_time(self):
        return f"pojutrze o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"

    def _info_on_weekday_at_time(self):
        if (
            TimeCalc._translate2polish(TimeCalc.weekday(self.event_datetime))
            == "wtorek"
        ):
            end = "e"
        else:
            end = ""
        return (
            f"w{end} {TimeCalc._translate2polish(TimeCalc.weekday(self.event_datetime))} "
            f"o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"
        )

    def _info_next_weekday_at_time(self):
        if (
            TimeCalc._translate2polish(TimeCalc.weekday(self.event_datetime))
            == "środę"
            or TimeCalc._translate2polish(TimeCalc.weekday(self.event_datetime))
            == "sobotę"
            or TimeCalc._translate2polish(TimeCalc.weekday(self.event_datetime))
            == "niedzielę"
        ):
            end = "ą"
        else:
            end = "y"
        return (
            f"w przyszł{end} {TimeCalc._translate2polish(TimeCalc.weekday(self.event_datetime))} "
            f"o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"
        )

    def show_info(self):
        if self._if_2omorrow():
            return self._info_tomorrow_at_time()
        if self._if_day_after_2omorrow():
            return self._info_day_after_2morrow_at_time()
        if self._if_this_week():
            return self._info_on_weekday_at_time()
        if self._if_next_week():
            return self._info_next_weekday_at_time()
        return self._show_detailed_info()

    def _show_detailed_info(self):
        true_values = TimeCalc._check_if_not_none(
            {
                "years": self._return_years_between(),
                "months": self._return_months_between(),
                "days": self._return_days_between(),
                "hours": self._return_hours_between(),
                "minutes": self._return_minutes_between(),
            }
        )
        if TimeCalc._info_if_years_is_true(true_values):
            return TimeCalc._info_if_years_is_true(true_values)
        if TimeCalc._info_if_months_is_true(true_values):
            return TimeCalc._info_if_months_is_true(true_values)
        if TimeCalc._info_if_no_years_no_months(true_values):
            return TimeCalc._info_if_no_years_no_months(true_values)
        return TimeCalc._info_if_only_hours_minutes(true_values)

    @staticmethod
    def _check_if_not_none(dict_):
        true_values = {}
        for key, value in dict_.items():
            if value:
                true_values.update({key: value})
        return true_values

    @staticmethod
    def _info_if_years_is_true(true_val):
        keys = true_val.keys()
        if "years" in keys:
            if "months" in keys:
                if "days" in keys:
                    return f"za {true_val['years']}, {true_val['months']} i {true_val['days']}"
                return f"za {true_val['years']} i {true_val['months']}"
            if "days" in keys:
                return f"za {true_val['years']} i {true_val['days']}"
            return f"za {true_val['years']}"

    @staticmethod
    def _info_if_months_is_true(true_values):
        keys = true_values.keys()
        if "months" in keys:
            if "days" in keys:
                return f"za {true_values['months']} i {true_values['days']}"
            return f"za {true_values['months']}"

    @staticmethod
    def _info_if_no_years_no_months(true_val):
        keys = true_val.keys()
        if "days" in keys:
            if "hours" in keys:
                if "minutes" in keys:
                    return f"za {true_val['days']}, {true_val['hours']} i {true_val['minutes']}"
                return f"za {true_val['days']} i {true_val['hours']}"
            if "minutes" in keys:
                return f"za {true_val['days']} i {true_val['minutes']}"
            return f"za {true_val['days']}"

    @staticmethod
    def _info_if_only_hours_minutes(true_values):
        keys = true_values.keys()
        if "hours" in keys:
            if "minutes" in keys:
                return f"za {true_values['hours']} i {true_values['minutes']}"
            return f"za {true_values['hours']}"
        if "minutes" in keys:
            return f"za {true_values['minutes']}"

    @staticmethod
    def _last_num_is_2_3_4(number):
        num2str = str(number)
        if int(num2str[-1]) in range(2, 5):
            return True

    @staticmethod
    def weekday(date_):
        return date_.strftime("%A")

    @staticmethod
    def days_in_month(date_):
        return date_.strftime("%-d")

    @staticmethod
    def event_time_in_hhmm_format(date_):
        return datetime.strftime(date_, "%H:%M")

    @staticmethod
    def _translate2polish(day_):
        weekdays = {
            "Monday": "poniedziałek",
            "Tuesday": "wtorek",
            "Wednesday": "środę",
            "Thursday": "czwartek",
            "Friday": "piątek",
            "Saturday": "sobotę",
            "Sunday": "niedzielę",
        }
        return weekdays.get(day_)
