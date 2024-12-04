import sqlite3
connection = sqlite3.connect('my_database.db')
cursor=None
def setConnection():
    cursor = connection.cursor()
