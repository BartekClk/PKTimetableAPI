from datetime import date
from math import ceil

class Week:
    def __init__(self):
        self.startMonth = 1
        self.startDay = 1
        self.weekType = None
        self.weekType = self.getWeekType()
        self.weekTypeEarly = self.getWeekType(earlyChange=True)

    def getWeekType(self, earlyChange = False):
        today = date.today()
        start_date = date(today.year, 1, 1)
        days_diff = (today - start_date).days + date(today.year,1,1).isoweekday() + (1 if earlyChange else 0)
        week_diff = ceil(days_diff/7)
        # return "P" if week_diff % 2 == 0 else "N" 
        return "N" if week_diff % 2 == 0 else "P" #Z jakiegoś powodu PK ma tygodnie na odwrót

    def get(self, earlyChange = False):
        weekType = self.weekTypeEarly if earlyChange else self.weekType
        return weekType

if __name__ == "__main__":
    week = Week()