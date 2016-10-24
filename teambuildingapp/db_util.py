import psycopg2
from config import *

def create_class(class_name, semester, instructor_username):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'INSERT INTO classes (class_name, class_semester, instructor_gt_username) VALUES (%s, %s, %s);'
    data = (class_name, semester, instructor_username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def create_team(class_id, gt_username, team_name):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'INSERT INTO teams (class_id, gt_username, team_name, is_captain) VALUES (%s, %s, %s, %s);'
    data = (class_id, gt_username, team_name, True)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def add_to_team(class_id, gt_username, team_name):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'INSERT INTO teams (class_id, gt_username, team_name, is_captain) VALUES (%s, %s, %s, %s);'
    data = (class_id, gt_username, team_name, False)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def remove_from_team(team_id, gt_username):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'DELETE FROM teams WHERE team_id = %s AND gt_username = %s;'
    data = (team_id, gt_username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def assign_team_captain(team_id, gt_username):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'UPDATE teams SET is_captain = %s WHERE team_id = %s;'
    data = (False, team_id)

    cur.execute(cmd, data)
    conn.commit()

    cmd = 'UPDATE teams SET is_captain = %s WHERE gt_username = %s;'
    data = (True, gt_username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def update_user_comment(username, comment):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'UPDATE users SET comment = %s WHERE username = %s;'
    data = (comment, username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def enroll_student(username, class_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'INSERT INTO rosters (class_id, gt_username) VALUES (%s, %s);'
    data = (class_id, username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def get_all_student_usernames():
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'SELECT gt_username FROM users WHERE is_instructor = FALSE'
    cur.execute(cmd)

    student_usernames = {x[0] for x in cur.fetchall()}

    cur.close()
    conn.close()

    return student_usernames

def register_user(username, is_instructor, email, first_name, last_name):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'INSERT INTO users (gt_username, is_instructor, email, first_name, last_name, comment) VALUES (%s, %s, %s, %s, %s, %s);'
    data = (username, is_instructor, email, first_name, last_name, '')

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def mass_register_users(userlist):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'INSERT INTO users (gt_username, is_instructor, email, first_name, last_name, comment) VALUES ' + '(%s, %s, %s, %s, %s, %s), '*(len(userlist)//6-1) + '(%s, %s, %s, %s, %s, %s);'
    cur.execute(cmd, userlist)
    conn.commit()

    cur.close()
    conn.close()

def enroll_from_roster(students, class_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    registered_students = get_all_student_usernames()

    roster_vals = ()
    registration_vals = ()
    for s in students:
        roster_vals  += (class_id, s[0])
        if s[0] not in registered_students:
            registration_vals += (s[0], False, s[1], s[2], s[3], '')

    mass_register_users(registration_vals)

    cmd = 'INSERT INTO rosters (class_id, gt_username) VALUES ' + '(%s, %s), '*(len(students)-1) + '(%s, %s);'
    cur.execute(cmd, roster_vals)
    conn.commit()

    cur.close()
    conn.close()