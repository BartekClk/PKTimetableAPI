from datetime import date

def timetableRow(row, day, lab, klab, jang, week, changes, changesData):
    data = {
        "id": row.id,
        "day": row.day,
        "hour": row.hour,
        "length": 1,
        "start": str(row.hours.start)[:-3],
        "end": str(row.hours.end)[:-3],
        "syllabusID": row.syllabusID,
        "syllabus": row.syllabus.name if row.syllabus else None,
        "lessonGroup": "",
        "lessonType": "",
        "lessonTypeFull": row.lessonType,
        "week": row.week,
        "lecturer": row.lecturer,
        "lecturerLink": row.lecturerLink,
        "hall": row.hall,
        "hallLink": row.hallLink,
        "altName": row.altName,
        "color": row.color,
    }
    
    if data is not None and day is not None and data["day"] != day: data = None

    if data is not None: 
        if data["lessonTypeFull"].lower()=="w":
            data["lessonType"] = "Wykład"
        data["lessonGroup"] = data["lessonTypeFull"][-1:] if (len(data["lessonTypeFull"]) > 1 and len(data["lessonTypeFull"])<4) else (data["lessonTypeFull"][-2:] if (len(data["lessonTypeFull"]) > 3 and len(data["lessonTypeFull"])<5) else "")
        data["lessonType"] = data["lessonTypeFull"][:1] if len(data["lessonTypeFull"]) > 1 else data["lessonType"]
        
    if data is not None and week is not None and week is not None and data["week"].lower() != week.lower(): data = None

    if changes is not None and data is not None:
        for row in changesData:
            today = date.today()
            start = row.start
            end = row.end
            if ((start - today).days <= 0 and (end - today).days >= 0) and row.syllabusID == data["syllabusID"]:
                if row.changesID == 1: 
                    conditionKeys = row.operation[0].keys()
                    hide = True
                    for key in conditionKeys:
                        hide = hide and (data[key] in row.operation[0][key] or -1 in row.operation[0][key])
                    if hide:
                        data = None
                elif row.changesID == 2:
                    conditionKeys = row.operation[0].keys()
                    change = True
                    for key in conditionKeys:
                        change = change and (data[key] in row.operation[0][key] or -1 in row.operation[0][key])
                    if change:
                        keys = row.operation[1].keys()
                        for key in keys:
                            data[key] = row.operation[1][key]

    if data is not None and lab is not None and data["lessonType"] == "L" and data["lessonGroup"] != str(lab): data = None
    if data is not None and klab is not None and data["lessonType"] == "K" and data["lessonGroup"] != str(klab): data = None
    if data is not None and jang is not None and jang is not "All" and data["syllabusID"] == 3 and data["lessonType"].find(str(jang).upper()) == -1: data = None

    return data