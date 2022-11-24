import sqlite3
import argparse

def main(dbname, output='schema.sql'):
    with sqlite3.connect(dbname)as con, open(output, 'w') as file:
        cursor = con.cursor()
        cursor.execute('select sql from sqlite_master')
        for r in cursor.fetchall():
            if r[0] is not None:
                file.write(r[0])
                file.write('\n\n')
        cursor.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Exports a SQLite datbase schema as SQL commands to a text file.",
        formatter_class=argparse.RawTextHelpFormatter)  # Preserves newlines in help text
    parser.add_argument('-d', '--dbname', required=False, default='anilist.db',
                        help="Filename of the SQLite database.")
    parser.add_argument('-o', '--output', required=False, default='schema.sql',
                        help="Filename to write to.")
    args = parser.parse_args()

    main(args.dbname, args.output)