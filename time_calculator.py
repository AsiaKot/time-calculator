from datetime import datetime, timedelta
from typing import Union, Tuple, Dict, NoReturn, KeysView


class TimeCalc:
    def __init__(self, event_datetime: datetime, reference_datetime: datetime = datetime.now()) -> NoReturn:
        self.event_datetime = event_datetime
        self.reference_datetime = reference_datetime

    def time_between(self) -> timedelta:
        return self.event_datetime - self.reference_datetime

    def __calc_years_months_days_between(self) -> Union[Tuple[int, int, int]]:
        event_year: int = self.event_datetime.year
        reference_year: int = self.reference_datetime.year
        event_month: int = self.event_datetime.month
        reference_month: int = self.reference_datetime.month
        event_day: int = self.event_datetime.day
        reference_day: int = self.reference_datetime.day

        if event_year >= reference_year:
            if event_month >= reference_month:
                return TimeCalc.__events_month_after_reference_month(
                    self.reference_datetime,
                    event_year,
                    reference_year,
                    event_month,
                    reference_month,
                    event_day,
                    reference_day,
                )
            return TimeCalc.__events_month_before_reference_month(
                self.reference_datetime,
                event_year,
                reference_year,
                event_month,
                reference_month,
                event_day,
                reference_day,
            )

    @staticmethod
    def __events_month_after_reference_month(
        reference_datetime: datetime,
        event_year: int,
        reference_year: int,
        event_month: int,
        reference_month: int,
        event_day: int,
        reference_day: int,
    ) -> Union[Tuple[int, int, int]]:
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
    def __events_month_before_reference_month(
        reference_datetime: datetime,
        event_year: int,
        reference_year: int,
        event_month: int,
        reference_month: int,
        event_day: int,
        reference_day: int
    ) -> Union[Tuple[int, int, int]]:
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

    def __if_2omorrow(self) -> bool:
        return self.time_between() / timedelta(minutes=1) <= 2879 and TimeCalc.weekday(
            self.event_datetime
        ) != TimeCalc.weekday(self.reference_datetime)

    def __if_day_after_2omorrow(self) -> bool:
        return 1441 <= self.time_between() / timedelta(minutes=1) <= 4319

    def __if_this_week(self) -> bool:
        return 4320 <= self.time_between() / timedelta(minutes=1) <= 10079

    def __if_next_week(self) -> bool:
        return 10080 <= self.time_between() / timedelta(minutes=1) <= 20159

    def __return_years_between(self) -> Union[str, None]:
        years_between: int = self.__calc_years_months_days_between()[0]
        if years_between == 0:
            return None
        elif years_between == 1:
            return "rok"
        elif years_between in range(2, 5):
            return f"{years_between} lata"
        return f"{years_between} lat"

    def __return_months_between(self) -> Union[str, None]:
        months_between: int = self.__calc_years_months_days_between()[1]
        if months_between == 0:
            return None
        elif months_between == 1:
            return "miesiąc"
        elif months_between in range(2, 5):
            return f"{months_between} miesiące"
        return f"{months_between} miesięcy"

    def __return_days_between(self) -> Union[str, None]:
        days_between: int = self.__calc_years_months_days_between()[2]
        if days_between == 0:
            return None
        elif days_between == 1:
            return f"{days_between} dzień"
        return f"{days_between} dni"

    def __return_hours_between(self) -> Union[str, None]:
        hours_between: int = int(
            self.time_between() % timedelta(minutes=1440) / timedelta(minutes=60)
        )
        if hours_between == 0:
            return None
        elif hours_between == 1:
            return "godzinę"
        elif TimeCalc.__last_num_is_2_3_4(hours_between) and hours_between != 12:
            ending = "y"
        else:
            ending = ""
        return f"{hours_between} godzin{ending}"

    def __return_minutes_between(self) -> Union[str, None]:
        minutes_between: int = int(
            self.time_between() % timedelta(minutes=60) / timedelta(minutes=1)
        )
        if minutes_between == 0:
            return None
        elif minutes_between == 1:
            return "minutę"
        elif TimeCalc.__last_num_is_2_3_4(minutes_between) and minutes_between != 12:
            ending = "y"
        else:
            ending = ""
        return f"{minutes_between} minut{ending}"

    def __info_tomorrow_at_time(self) -> str:
        return f"jutro o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"

    def __info_day_after_2morrow_at_time(self) -> str:
        return f"pojutrze o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"

    def _info_on_weekday_at_time(self) -> str:
        if (
            TimeCalc.__translate2polish(TimeCalc.weekday(self.event_datetime))
            == "wtorek"
        ):
            end = "e"
        else:
            end = ""
        return (
            f"w{end} {TimeCalc.__translate2polish(TimeCalc.weekday(self.event_datetime))} "
            f"o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"
        )

    def __info_next_weekday_at_time(self) -> str:
        if (
            TimeCalc.__translate2polish(TimeCalc.weekday(self.event_datetime))
            == "środę"
            or TimeCalc.__translate2polish(TimeCalc.weekday(self.event_datetime))
            == "sobotę"
            or TimeCalc.__translate2polish(TimeCalc.weekday(self.event_datetime))
            == "niedzielę"
        ):
            end = "ą"
        else:
            end = "y"
        return (
            f"w przyszł{end} {TimeCalc.__translate2polish(TimeCalc.weekday(self.event_datetime))} "
            f"o {TimeCalc.event_time_in_hhmm_format(self.event_datetime)}"
        )

    def show_info(self) -> str:
        if self.__if_2omorrow():
            return self.__info_tomorrow_at_time()
        elif self.__if_day_after_2omorrow():
            return self.__info_day_after_2morrow_at_time()
        elif self.__if_this_week():
            return self._info_on_weekday_at_time()
        elif self.__if_next_week():
            return self.__info_next_weekday_at_time()
        return self.__show_detailed_info()

    def __show_detailed_info(self) -> str:
        true_values: Dict = TimeCalc.__check_if_not_none(
            {
                "years": self.__return_years_between(),
                "months": self.__return_months_between(),
                "days": self.__return_days_between(),
                "hours": self.__return_hours_between(),
                "minutes": self.__return_minutes_between(),
            }
        )
        if TimeCalc.__info_if_years_is_true(true_values):
            return TimeCalc.__info_if_years_is_true(true_values)
        elif TimeCalc.__info_if_months_is_true(true_values):
            return TimeCalc.__info_if_months_is_true(true_values)
        elif TimeCalc.__info_if_no_years_no_months(true_values):
            return TimeCalc.__info_if_no_years_no_months(true_values)
        return TimeCalc.__info_if_only_hours_minutes(true_values)

    @staticmethod
    def __check_if_not_none(dict_: Dict) -> Dict:
        true_values: dict = {}
        for key, value in dict_.items():
            if value:
                true_values.update({key: value})
        return true_values

    @staticmethod
    def __info_if_years_is_true(true_val: Dict) -> str:
        keys: KeysView = true_val.keys()
        if "years" in keys:
            if "months" in keys:
                if "days" in keys:
                    return f"za {true_val['years']}, {true_val['months']} i {true_val['days']}"
                return f"za {true_val['years']} i {true_val['months']}"
            if "days" in keys:
                return f"za {true_val['years']} i {true_val['days']}"
            return f"za {true_val['years']}"

    @staticmethod
    def __info_if_months_is_true(true_val: Dict) -> str:
        keys: KeysView = true_val.keys()
        if "months" in keys:
            if "days" in keys:
                return f"za {true_val['months']} i {true_val['days']}"
            return f"za {true_val['months']}"

    @staticmethod
    def __info_if_no_years_no_months(true_val: Dict) -> str:
        keys: KeysView = true_val.keys()
        if "days" in keys:
            if "hours" in keys:
                if "minutes" in keys:
                    return f"za {true_val['days']}, {true_val['hours']} i {true_val['minutes']}"
                return f"za {true_val['days']} i {true_val['hours']}"
            if "minutes" in keys:
                return f"za {true_val['days']} i {true_val['minutes']}"
            return f"za {true_val['days']}"

    @staticmethod
    def __info_if_only_hours_minutes(true_val: Dict) -> str:
        keys: KeysView = true_val.keys()
        if "hours" in keys:
            if "minutes" in keys:
                return f"za {true_val['hours']} i {true_val['minutes']}"
            return f"za {true_val['hours']}"
        if "minutes" in keys:
            return f"za {true_val['minutes']}"

    @staticmethod
    def __last_num_is_2_3_4(number: int) -> bool:
        return int(str(number)[-1]) in range(2, 5)

    @staticmethod
    def weekday(date_: datetime) -> str:
        return date_.strftime("%A")

    @staticmethod
    def days_in_month(date_: datetime) -> int:
        return int(date_.strftime("%-d"))

    @staticmethod
    def event_time_in_hhmm_format(date_: datetime) -> str:
        return datetime.strftime(date_, "%H:%M")

    @staticmethod
    def __translate2polish(day_: str) -> str:
        weekdays: Dict[str: str] = {
            "Monday": "poniedziałek",
            "Tuesday": "wtorek",
            "Wednesday": "środę",
            "Thursday": "czwartek",
            "Friday": "piątek",
            "Saturday": "sobotę",
            "Sunday": "niedzielę",
        }
        return weekdays.get(day_)
