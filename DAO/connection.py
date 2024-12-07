from utils.config import LOG_DIR, DBNAME, LOG_LEVEL
import sqlite3


def initDatabase():
    global connection
    try:
        connection = sqlite3.connect(DBNAME)
        cursor = connection.cursor()
        sql = 'create table if not exists Loaded_log( id integer primary key autoincrement, filename text not null, dateload timestamp default current_timestamp)'
        cursor.execute(sql)
        sql = 'create table if not exists dictionary_events (id integer  primary key autoincrement,  value TEXT not null unique)'

        cursor.execute(sql)
        try:
            sql = 'insert into  dictionary_events (value) values ("INFO")'
            cursor.execute(sql)
        except Exception as e:
            pass
        try:
            sql = 'insert into  dictionary_events (value) values ("ERROR")'
            cursor.execute(sql)
        except Exception:
            pass
        sql = 'create table if not exists log_event (ID integer primary key autoincrement, date TEXT, event TEXT not null, log_id integer,    event_class integer,  foreign key (event_class) references dictionary_events(ID), foreign key(log_id) references Loaded_log(ID))'
        cursor.execute(sql)

    finally:
        connection.commit()
        connection.close()
def load_log(filename):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()


