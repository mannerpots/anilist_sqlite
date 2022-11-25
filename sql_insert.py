import sqlite3

LIST_DATA_INSERT = '''INSERT or IGNORE
                        INTO "main"."ListDataHistorical" 
                        ("ID", "Title", "TitleRomaji", "MediaType", "Format",
                        "Score", "Status", "Progress", "Episodes", "Repeat",
                        "StartedAt", "CompletedAt", "UpdatedAt", "Notes", "HiddenFromStatusList")
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date(?), date(?), datetime(?, 'unixepoch'), ?, ?);'''

CUSTOM_LISTS_INSERT = '''INSERT or IGNORE
                            INTO "main"."CustomListMembershipHistorical" 
                            ("ID", "UpdatedAt", "CustomList", "IsMember") 
                            VALUES (?, datetime(?, 'unixepoch'), ?, ?);'''

def insert_custom_lists(cursor: sqlite3.Connection,
                        id: int,
                        updated_at: int,
                        custom_lists_membership: dict[str, bool]) -> None:
    """Inserts an entry into the CustomListMembershipHistorical table for each pair in the given dictionary."""
    for list, is_memeber in custom_lists_membership.items():
        cursor.execute(CUSTOM_LISTS_INSERT, (
            id,
            updated_at,
            list,
            is_memeber
            ))

def insert_media(cursor: sqlite3.Connection, media_info: dict):
    """Inserts an entry into the ListDataHistorical table."""
    date_started = (f"{media_info['startedAt']['year']}"
                    f"-{media_info['startedAt']['month']}"
                    f"-{media_info['startedAt']['day']}")
    date_completed = (f"{media_info['completedAt']['year']}"
                      f"-{media_info['completedAt']['month']}"
                      f"-{media_info['completedAt']['day']}")

    cursor.execute(LIST_DATA_INSERT, (
        media_info['media']['id'], 
        media_info['media']['title']['english'],
        media_info['media']['title']['romaji'],
        media_info['media']['type'],
        media_info['media']['format'],
        media_info['score'],
        media_info['status'],
        media_info['progress'],
        media_info['media']['episodes'], 
        media_info['repeat'],
        date_started,
        date_completed,
        media_info['updatedAt'],
        media_info['notes'],
        media_info['hiddenFromStatusLists'],
        ))

    if media_info['customLists'] is not None:
        insert_custom_lists(cursor, media_info['media']['id'], media_info['updatedAt'], media_info['customLists'])
