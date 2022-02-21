from datetime import datetime, timedelta


class TimeCalc:
    def __init__(self, event_datetime, reference_datetime=datetime.now()):
        self.event_datetime = event_datetime
        self.reference_datetime = reference_datetime

    def time_between(self):
        time_between = self.event_datetime - self.reference_datetime
        return time_between

    def if_2omorrow(self):
        if self.time_between() / timedelta(minutes=1) <= 2879 and \
                TimeCalc.weekday(self.event_datetime) != TimeCalc.weekday(self.reference_datetime):
            return True

    def if_day_after_2omorrow(self):
        if 1441 <= self.time_between() / timedelta(minutes=1) <= 4319:
            return True

    def if_this_week(self):
        if 4320 <= self.time_between() / timedelta(minutes=1) <= 10079:
            return True

    def if_next_week(self):
        if 10080 <= self.time_between() / timedelta(minutes=1) <= 20159:
            return True

    def calc_years_between(self):
        years_between = int(self.time_between() / timedelta(days=365))
        if years_between == 0:
            return None
        if years_between == 1:
            return f"rok"
        if years_between in range(2, 5):
            return f"{years_between} lata"
        return f"{years_between} lat"

    def calc_months_between(self):
        months_between = int(self.time_between() % timedelta(days=365) / timedelta(days=30))
        if months_between == 0:
            return None
        if months_between == 1:
            return f"miesiąc"
        if months_between in range(2, 5):
            return f"{months_between} miesiące"
        return f"{months_between} miesięcy"

    def calc_days_between(self):
        days_between = int(self.time_between() % timedelta(days=30) / timedelta(days=1))
        if days_between == 0:
            return None
        if days_between == 1:
            return f"{days_between} dzień"
        return f"{days_between} dni"

    def calc_hours_between(self):
        hours_between = int(self.time_between() % timedelta(minutes=1440) / timedelta(minutes=60))
        if hours_between == 0:
            return None
        if hours_between == 1:
            return "godzinę"
        if TimeCalc.last_num_is_2_3_4(hours_between):
            ending = "y"
        else:
            ending = ""
        return f"{hours_between} godzin{ending}"

    def calc_minutes_between(self):
        minutes_between = int(self.time_between() % timedelta(minutes=60) / timedelta(minutes=1))
        if minutes_between == 0:
            return None
        if minutes_between == 1:
            return "minutę"
        if TimeCalc.last_num_is_2_3_4(minutes_between):
            ending = "y"
        else:
            ending = ""
        return f"{minutes_between} minut{ending}"

    def show_info(self):
        if self.if_2omorrow():
            return f"jutro o {TimeCalc.event_time(self.event_datetime)}"
        elif self.if_day_after_2omorrow():
            return f"pojutrze o {TimeCalc.event_time(self.event_datetime)}"
        elif self.if_this_week():
            if TimeCalc.translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "wtorek":
                ending = "e"
            else:
                ending = ""
            return f"w{ending} {TimeCalc.translate_weekday2polish(TimeCalc.weekday(self.event_datetime))} " \
                   f"o {TimeCalc.event_time(self.event_datetime)}"
        elif self.if_next_week():
            if TimeCalc.translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "środę" or \
                    TimeCalc.translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "sobotę" or \
                    TimeCalc.translate_weekday2polish(TimeCalc.weekday(self.event_datetime)) == "niedzielę":
                ending = "ą"
            else:
                ending = "y"
            return f"w przyszł{ending} {TimeCalc.translate_weekday2polish(TimeCalc.weekday(self.event_datetime))} " \
                   f"o {TimeCalc.event_time(self.event_datetime)}"
        else:
            years = self.calc_years_between()
            months = self.calc_months_between()
            days = self.calc_days_between()
            hours = self.calc_hours_between()
            minutes = self.calc_minutes_between()
            if years and months and days:
                return f"za {years}, {months} i {days}"
            if years and months:
                return f"za {years} i {months}"
            if years and days:
                return f"za {years} i {days}"
            if months and days:
                return f"za {months} i {days}"
            elif days and hours and minutes:
                return f"za {days}, {hours} i {minutes}"
            elif days and hours:
                return f"za {days} i {hours}"
            elif days and minutes:
                return f"za {days} i {minutes}"
            elif hours and minutes:
                return f"za {hours} i {minutes}"
            if years:
                return f"za {years}"
            elif months:
                return f"za {months}"
            elif days:
                return f"za {days}"
            elif hours:
                return f"za {hours}"
            elif minutes:
                return f"za {minutes}"

    @staticmethod
    def last_num_is_2_3_4(number):
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
    def translate_weekday2polish(day_):
        weekdays = {"Monday": "poniedziałek", "Tuesday": "wtorek", "Wednesday": "środę", "Thursday": "czwartek",
                    "Friday": "piątek", "Saturday": "sobotę", "Sunday": "niedzielę"}
        return weekdays.get(day_)
