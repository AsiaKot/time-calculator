from datetime import datetime, timedelta


class TimeCalc:
    def __init__(self, event_datetime, reference_datetime=datetime.now()):
        self.event_datetime = event_datetime
        self.reference_datetime = reference_datetime

    def time_between(self):
        time_between = self.event_datetime - self.reference_datetime
        return time_between

    def _if_2omorrow(self):
        if self.time_between() / timedelta(minutes=1) <= 2879 and \
                TimeCalc.weekday(self.event_datetime) != TimeCalc.weekday(self.reference_datetime):
            return True

    def _if_day_after_2omorrow(self):
        if 1441 <= self.time_between() / timedelta(minutes=1) <= 4319:
            return True

    def _if_this_week(self):
        if 4320 <= self.time_between() / timedelta(minutes=1) <= 10079:
            return True

    def _if_next_week(self):
        if 10080 <= self.time_between() / timedelta(minutes=1) <= 20159:
            return True

    def _calc_years_between(self):
        years_between = int(self.time_between() / timedelta(days=365))
        if years_between == 0:
            return None
        if years_between == 1:
            return f"rok"
        if years_between in range(2, 5):
            return f"{years_between} lata"
        return f"{years_between} lat"

    def _calc_months_between(self):
        months_between = int(self.time_between() % timedelta(days=365) / timedelta(days=30))
        if months_between == 0:
            return None
        if months_between == 1:
            return f"miesiąc"
        if months_between in range(2, 5):
            return f"{months_between} miesiące"
        return f"{months_between} miesięcy"

    def _calc_days_between(self):
        days_between = int(self.time_between() % timedelta(days=30) / timedelta(days=1))
        if days_between == 0:
            return None
        if days_between == 1:
            return f"{days_between} dzień"
        return f"{days_between} dni"

    def _calc_hours_between(self):
        hours_between = int(self.time_between() % timedelta(minutes=1440) / timedelta(minutes=60))
        if hours_between == 0:
            return None
        if hours_between == 1:
            return "godzinę"
        if TimeCalc._last_num_is_2_3_4(hours_between):
            ending = "y"
        else:
            ending = ""
        return f"{hours_between} godzin{ending}"

    def _calc_minutes_between(self):
        minutes_between = int(self.time_between() % timedelta(minutes=60) / timedelta(minutes=1))
        if minutes_between == 0:
            return None
        if minutes_between == 1:
            return "minutę"
        if TimeCalc._last_num_is_2_3_4(minutes_between):
            ending = "y"
        else:
            ending = ""
        return f"{minutes_between} minut{ending}"

    def _tomorrow_at_time(self):
        return f"jutro o {TimeCalc.event_time(self.event_datetime)}"

    def _day_after_2morrow_at_time(self):
        return f"pojutrze o {TimeCalc.event_time(self.event_datetime)}"

    def _on_weekday_at_time(self):
        if TimeCalc._translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "wtorek":
            ending = "e"
        else:
            ending = ""
        return f"w{ending} {TimeCalc._translate_weekday2polish(TimeCalc.weekday(self.event_datetime))} " \
               f"o {TimeCalc.event_time(self.event_datetime)}"

    def _next_weekday_at_time(self):
        if TimeCalc._translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "środę" or \
                TimeCalc._translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "sobotę" or \
                TimeCalc._translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "niedzielę":
            ending = "ą"
        else:
            ending = "y"
        return f"w przyszł{ending} {TimeCalc._translate_weekday2polish(TimeCalc.weekday(self.event_datetime))} " \
               f"o {TimeCalc.event_time(self.event_datetime)}"

    def _show_detailed_info(self):
        true_values = TimeCalc._check_if_not_none(
            {
            "years": self._calc_years_between(),
            "months": self._calc_months_between(),
            "days": self._calc_days_between(),
            "hours": self._calc_hours_between(),
            "minutes": self._calc_minutes_between()
            }
        )
        if TimeCalc._if_years_is_true(true_values):
            return TimeCalc._if_years_is_true(true_values)
        elif TimeCalc._if_months_is_true(true_values):
            return TimeCalc._if_months_is_true(true_values)
        elif TimeCalc._if_no_years_no_months(true_values):
            return TimeCalc._if_no_years_no_months(true_values)
        else:
            return TimeCalc._if_only_hours_minutes(true_values)

    @staticmethod
    def _check_if_not_none(dict_):
        true_values = {}
        for key, value in dict_.items():
            if value:
                true_values.update({key: value})
        return true_values

    @staticmethod
    def _if_years_is_true(true_values):
        keys = true_values.keys()
        if "years" in keys:
            if "months" in keys:
                if "days" in keys:
                    return f"za {true_values['years']}, {true_values['months']} i {true_values['days']}"
                return f"za {true_values['years']} i {true_values['months']}"
            if "days" in keys:
                return f"za {true_values['years']} i {true_values['days']}"
            return f"za {true_values['years']}"

    @staticmethod
    def _if_months_is_true(true_values):
        keys = true_values.keys()
        if "months" in keys:
            if "days" in keys:
                return f"za {true_values['months']} i {true_values['days']}"
            return f"za {true_values['months']}"

    @staticmethod
    def _if_no_years_no_months(true_values):
        keys = true_values.keys()
        if "days" in keys:
            if "hours" in keys:
                if "minutes" in keys:
                    return f"za {true_values['days']}, {true_values['hours']} i {true_values['minutes']}"
                return f"za {true_values['days']} i {true_values['hours']}"
            if "minutes" in keys:
                return f"za {true_values['days']} i {true_values['minutes']}"
            return f"za {true_values['days']}"

    @staticmethod
    def _if_only_hours_minutes(true_values):
        keys = true_values.keys()
        if "hours" in keys:
            if "minutes" in keys:
                return f"za {true_values['hours']} i {true_values['minutes']}"
            return f"za {true_values['hours']}"
        if "minutes" in keys:
            return f"za {true_values['minutes']}"

    def show_info(self):
        if self._if_2omorrow():
            return self._tomorrow_at_time()
        elif self._if_day_after_2omorrow():
            return self._day_after_2morrow_at_time()
        elif self._if_this_week():
            return self._on_weekday_at_time()
        elif self._if_next_week():
            return self._next_weekday_at_time()
        return self._show_detailed_info()

    @staticmethod
    def _last_num_is_2_3_4(number):
        num2str = str(number)
        if int(num2str[-1]) in range(2, 5):
            return True

    @staticmethod
    def weekday(date_):
        return date_.strftime("%A")

    @staticmethod
    def event_time(date_):
        return datetime.strftime(date_, '%H:%M')

    @staticmethod
    def _translate_weekday2polish(day_):
        weekdays = {"Monday": "poniedziałek", "Tuesday": "wtorek", "Wednesday": "środę", "Thursday": "czwartek",
                    "Friday": "piątek", "Saturday": "sobotę", "Sunday": "niedzielę"}
        return weekdays.get(day_)



d1 = datetime(2032, 12, 31, 23, 59)
d2 = datetime(2022, 1, 1, 00, 00)

TimeCalc(d1, d2).show_info()