import sqlite3


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS scores(day TEXT, month TEXT, year TEXT, wpm TEXT, name TEXT)')


if __name__ == "__main__":
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    create_table()
