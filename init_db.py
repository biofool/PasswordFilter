import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('User1', 'User1Password')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('User1', 'User1Password')
            )

connection.commit()
connection.close()
