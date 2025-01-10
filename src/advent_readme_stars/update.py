from typing import List

from advent_readme_stars.constants import (
    ADVENT_URL,
    HEADER_PREFIX,
    STAR_SYMBOL,
    TABLE_MARKER,
    YEAR,
    SHOW_MISSING_DAYS,
    SHOW_ALL_MISSING_DAYS
)
from advent_readme_stars.progress import get_progress, DayProgress


def remove_existing_table(lines: List[str]) -> List[str]:
    """
    If there's an existing table, it should be between two table markers.
    If that's the case, remove the existing table and return a single table
    marker in its place. If not, just return the original content.
    """
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None and line.strip() == TABLE_MARKER:
            start = i
            continue
        if start is not None and line.strip() == TABLE_MARKER:
            end = i
            break

    if start is not None and end is not None:
        return lines[:start] + lines[end:]
    return lines


def insert_table(lines: List[str]) -> List[str]:
    """
    Search the lines for a table marker, and insert a table there.
    """
    table_location = None
    for i, line in enumerate(lines):
        if line.strip() == TABLE_MARKER:
            table_location = i
            break
    else:
        return lines

    to_insert = [
        TABLE_MARKER,
        f"{HEADER_PREFIX} {YEAR} Results",
        "",
        "| Day | Part 1 | Part 2 |",
        "| :---: | :---: | :---: |",
    ]
    stars_info = sorted(list(get_progress()), key=lambda p: p.day)
    print(stars_info)

    if SHOW_MISSING_DAYS or SHOW_ALL_MISSING_DAYS :
        first_day = 1 if SHOW_ALL_MISSING_DAYS or not stars_info else stars_info[0].day
        current_day = first_day

        for day in stars_info.copy():
            index = stars_info.index(day)
            if day.day != current_day:
                while current_day < day.day:
                    stars_info.insert(index, DayProgress(current_day, False, False))
                    current_day += 1
                    index += 1

            current_day += 1

        print(stars_info)

        if SHOW_ALL_MISSING_DAYS and (not stars_info or stars_info[-1].day != 25):
            for i in range(stars_info[-1].day, 25):
                stars_info.append(DayProgress(i, False, False))

    print(stars_info)

    for star_info in stars_info:
        day_url = f"{ADVENT_URL}/{YEAR}/day/{star_info.day}"
        day_text = f"[Day {star_info.day}]({day_url})"
        part_1_text = STAR_SYMBOL if star_info.part_1 else " "
        part_2_text = STAR_SYMBOL if star_info.part_2 else " "
        to_insert.append(f"| {day_text} | {part_1_text} | {part_2_text} |")

    return lines[:table_location] + to_insert + lines[table_location:]


def update_readme(readme: List[str]) -> List[str]:
    """
    Take the contents of a readme file and update them
    """
    reduced = remove_existing_table(readme)
    new_readme = insert_table(reduced)

    return new_readme
