import psycopg2
from config import *

def setup_tables():
    tables = get_tables()
    print('Found tables:{}'.format(tables))
    if 'users' not in tables:
        print('Users table not found, creating one...')
        setup_users_table()

    if 'classes' not in tables:
        print('Classes table not found, creating one...')
        setup_classes_table()

    if 'rosters' not in tables:
        print('Rosters table not found, creating one...')
        setup_rosters_table()

    if 'teams' not in tables:
        print('Teams table not found, creating one...')
        setup_teams_table()

def get_tables():
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    cur.close()
    return [x[0] for x in tables]

def setup_users_table():
    cur = conn.cursor()

    cmd = """CREATE TABLE USERS(
   GT_USERNAME    TEXT PRIMARY KEY     NOT NULL,
   IS_INSTRUCTOR  BOOL                 NOT NULL,
   EMAIL          TEXT                 NOT NULL,
   FIRST_NAME     TEXT                 NOT NULL,
   LAST_NAME      TEXT                 NOT NULL,
   COMMENT        TEXT
);"""

    cur.execute(cmd)
    conn.commit()

    cur.close()


def setup_teams_table():
    cur = conn.cursor()

    cmd = """CREATE TABLE TEAMS(
   TEAM_ID        SERIAL               NOT NULL,
   CLASS_ID       INTEGER              NOT NULL REFERENCES CLASSES (CLASS_ID),
   GT_USERNAME    TEXT                 NOT NULL REFERENCES USERS(GT_USERNAME),
   TEAM_NAME      TEXT                 NOT NULL,
   IS_CAPTAIN     BOOL                 NOT NULL,
   COMMENT        TEXT,
   PRIMARY KEY(TEAM_ID, CLASS_ID, GT_USERNAME)
);"""

    cur.execute(cmd)
    conn.commit()

    cur.close()

def setup_classes_table():
    cur = conn.cursor()

    cmd = """CREATE TABLE CLASSES(
   CLASS_ID                  SERIAL              NOT NULL UNIQUE,
   INSTRUCTOR_GT_USERNAME    TEXT                REFERENCES USERS (GT_USERNAME),
   CLASS_NAME                TEXT                NOT NULL,
   CLASS_SEMESTER            TEXT                NOT NULL,
   PRIMARY KEY(CLASS_NAME, CLASS_SEMESTER)
);"""

    cur.execute(cmd)
    conn.commit()

    cur.close()

def setup_rosters_table():
    cur = conn.cursor()

    cmd = """CREATE TABLE ROSTERS(
   CLASS_ID                  INTEGER              NOT NULL REFERENCES CLASSES (CLASS_ID),
   GT_USERNAME               TEXT                 NOT NULL REFERENCES USERS (GT_USERNAME),
   PRIMARY KEY(CLASS_ID, GT_USERNAME)
);"""

    cur.execute(cmd)
    conn.commit()

    cur.close()

def main():
    global conn
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    setup_tables()


    conn.close()

main()