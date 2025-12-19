def mergeLessons(table, hours):
    if not table:
        return []

    merged = []
    i = 0

    while i < len(table):
        current = table[i]
        lesson_length = 1

        while (
            i + lesson_length < len(table)
            and current["syllabusID"] == table[i + lesson_length]["syllabusID"]
            and current["week"] == table[i + lesson_length]["week"]
            and current["lessonTypeFull"] == table[i + lesson_length]["lessonTypeFull"]
            and current["lecturer"] == table[i + lesson_length]["lecturer"]
            and current["hall"] == table[i + lesson_length]["hall"]
            and current["hour"] + lesson_length == table[i + lesson_length]["hour"]
            and current["lessonTypeFull"] == table[i + lesson_length]["lessonTypeFull"]
        ):
            lesson_length += 1

        merged_lesson = current.copy()
        merged_lesson["length"] = lesson_length

        if merged_lesson["id"] != -1:
            merged_lesson["end"] = str(hours[int(merged_lesson["hour"] + (lesson_length - 1))]["end"])[:-3]
        else:
            merged_lesson["end"] = str(table[i + lesson_length - 1]["end"])
            merged_lesson["exactEnd"] = str(table[i + lesson_length - 1]["exactEnd"])

        merged.append(merged_lesson)
        i += lesson_length 

    return merged
