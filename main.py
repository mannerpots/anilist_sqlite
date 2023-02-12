import argparse
import sqlite3

from anilist_tools.upcoming_sequels import get_user_id_by_name

from get_list import get_user_media, MediaType, MediaStatus
from sql_insert import insert_media


def main(username: str, dbname:str):
    failed_count = 0
    dbname = 'anilist.db'
    user_id = get_user_id_by_name(username)
    user_media_list = get_user_media(user_id)
    with sqlite3.connect(dbname) as conn:
        for entry in user_media_list:
            insert_media(conn.cursor(), entry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given an anilist username, agets their list data and inserts it into a SQLite database.",
        formatter_class=argparse.RawTextHelpFormatter)  # Preserves newlines in help text
    parser.add_argument('-u', '--username', required=True,
                        help="User whose list should be checked.")
    parser.add_argument('-d', '--database', required=True,
                        help="The SQLite datbase ot insert into.")
    args = parser.parse_args()

    main(args.username, args.database)