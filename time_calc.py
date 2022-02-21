from datetime import datetime, timedelta

'''
Napisanie funkcji (lub metody klasy), która jako argumenty dostaje czas i datę zdarzenia oraz czas i datę odniesienia
(domyślnie ustawioną na chwilę obecną) i zwraca tekst w języku naturalnym, po polsku,
który opisuje względny czas zdarzenia, np.:

jutro o 15:20
za 5 godzin i 13 minut
w przyszły poniedziałek o 14:00
przedwczoraj o 20:00
za miesiąc 3 dni i 5 godzin
'''


class TimeCalc:
    def __init__(self, event_datetime, reference_datetime=datetime.now()):
        self.event_datetime = event_datetime
        self.reference_datetime = reference_datetime

    def event_time(self):
        return datetime.strftime(self.event_datetime, '%H:%M')

    def event_weekday(self):
        return self.event_datetime.strftime("%A")

    def translate_weekday2polish(self):
        weekdays = {"Monday": "poniedziałek", "Tuesday": "wtorek", "Wednesday": "środę", "Thursday": "czwartek",
                    "Friday": "piątek", "Saturday": "sobotę", "Sunday": "niedzielę"}
        return weekdays.get(self.event_weekday())

    def event_month(self):
        return self.event_datetime.strftime("%B")

    def calc_time_between(self):
        time_between = self.event_datetime - self.reference_datetime
        return time_between

    def calc_total_minutes_between(self):
        total_minutes_between = int((self.event_datetime - self.reference_datetime).total_seconds() / 60)
        return total_minutes_between

    def convert_time(self):
        time_between = self.calc_time_between()
        years = int(time_between / timedelta(days=365))
        months = int(time_between % timedelta(days=365) / timedelta(days=30))
        days = int(time_between % timedelta(days=30) / timedelta(days=1))
        hours = int(time_between % timedelta(days=1) / timedelta(minutes=60))
        minutes = int(time_between % timedelta(minutes=60) / timedelta(minutes=1))

        return {"years": years, "months": months, "days": days, "hours": hours, "minutes": minutes}

    def event_is_this_week(self):
        days = self.convert_time().get('days')
        if self.convert_time().get("years") == 0 and self.convert_time().get("months") == 0 and days <= 7:
            if 0 <= days <= 1 and self.event_weekday() == self.reference_datetime.strftime("%A"):
                return f"za {self.convert_time().get('hours')} godzin/y i {self.convert_time().get('minutes')} minut/y"
            elif 0 <= days <= 1 and self.event_weekday() != self.reference_datetime.strftime("%A"):
                return f"jutro o {self.event_time()}"
            elif days == 2:
                return f"pojutrze o {self.event_time()}"
            elif 3 <= days <= 7:
                return f"w {self.translate_weekday2polish()} o {self.event_time()}"

    def event_is_next_week(self):
        if self.convert_time().get("years") == 0 and self.convert_time().get("months") == 0 \
                and 7 < self.convert_time().get("days") <= 14:
            return f"w przyszły/ą {self.translate_weekday2polish()} o {self.event_time()}"

    def event_is_this_month(self):
        days = self.convert_time().get("days")
        hours = self.convert_time().get("hours")
        minutes = self.convert_time().get("minutes")
        if self.convert_time().get("years") == 0 and self.event_month() == self.reference_datetime.strftime("%B"):
            if 14 < days <= 30:
                return f"za {days} dni, {hours} godzin/y i {minutes} minut/y"
            elif self.convert_time().get("months") == 1 and days == 0:
                return f"za 30 dni, {hours} godzin/y i {minutes} minut/y"

    def event_is_next_month(self):
        months = self.convert_time().get("months")
        days = self.convert_time().get("days")
        hours = self.convert_time().get("hours")
        minutes = self.convert_time().get("minutes")
        if self.convert_time().get("years") == 0:
            if months == 1 and self.event_month() != self.reference_datetime.strftime("%B"):
                return f"za miesiąc, {days} dzień/dni, {hours} godzin/y i {minutes} minut/y"
            elif months == 1 and self.event_month() == self.reference_datetime.strftime("%B"):
                return f"za miesiąc, {days} dzień/dni, {hours} godzin/y i {minutes} minut/y"
            elif 1 < months <= 12 and self.event_month() != self.reference_datetime.strftime("%B"):
                return f"za {months} miesiąc/miesiące/miesięcy, {days} dzień/dni, {hours} godzin/y i {minutes} minut/y"

    def event_is_in_next_years(self):
        years = self.convert_time().get("years")
        months = self.convert_time().get("months")
        days = self.convert_time().get("days")
        if 0 < years == 1:
            return f"za rok, {months} miesiąc/miesiące/miesięcy i {days} dzień/dni"
        elif years > 1:
            return f"za {years} lat/a, {months} miesiąc/miesiące/miesięcy i {days} dzień/dni"

    def print_info(self):
        if self.event_is_this_week():
            print(self.event_is_this_week())
        elif self.event_is_next_week():
            print(self.event_is_next_week())
        elif self.event_is_this_month():
            print(self.event_is_this_month())
        elif self.event_is_next_month():
            print(self.event_is_next_month())
        elif self.event_is_in_next_years():
            print(self.event_is_in_next_years())


reference_date = datetime(2022, 1, 1, 00, 00)
event_datetime = datetime(2023, 12, 31, 23, 59)

event = TimeCalc(event_datetime, reference_date)
event.print_info()

print(event.convert_time())
