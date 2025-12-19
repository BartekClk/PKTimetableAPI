def fillBreaks(table, hours):
    def findLesson(timetable, day, hour):
        return next(
            (lesson for lesson in timetable if lesson['day'] == day and lesson['hour'] == hour), 
            None
        )
    
    filled = table.copy()
    nhours = 16 

    for d in range(1, 6): 
        day_schedule = []
        for h in range(1, nhours):
            lesson = findLesson(table, d, h)
            day_schedule.append(lesson if lesson is None else lesson["syllabusID"])

        while day_schedule and day_schedule[-1] is None:
            day_schedule.pop()

        has_lesson_before = False
        for i, el in enumerate(day_schedule):
            if el is None:
                if not has_lesson_before:
                    continue

                start = None
                end = None
                if i > 0 and str(hours[i+1]["start"]) != str(hours[i]["end"]):
                    start = str(hours[i]["end"])
                if i + 2 <= nhours and str(hours[i+1]["end"]) != str(hours[i+2]["start"]):
                    end = str(hours[i+2]["start"])

                filled.append({
                    "id": -1,
                    "day": d,
                    "hour": i+1,
                    "length": 1,
                    "start": str(hours[i+1]["start"])[:-3],
                    "exactStart": start[:-3] if start is not None else str(hours[i+1]["start"])[:-3],
                    "end": str(hours[i+1]["end"])[:-3],
                    "exactEnd": end[:-3] if end is not None else str(hours[i+1]["start"])[:-3],
                    "syllabusID": 2,
                    "syllabus": "Przerwa",
                    "lessonGroup": "",
                    "lessonType": "",
                    "lessonTypeFull": "",
                    "week": "",
                    "lecturer": "",
                    "lecturerLink": "",
                    "hall": "",
                    "hallLink": "",
                    "altName": "",
                })
            else:
                has_lesson_before = True

    return filled
