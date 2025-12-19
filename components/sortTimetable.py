def sortTimetable (timetable):
    return sorted(timetable, key=lambda x: (x.get('day', 0), x.get('hour', 0)))