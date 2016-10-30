import psycopg2
from teambuildingapp.config import *

def get_user_info(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT is_instructor, email, first_name, last_name, comment FROM users WHERE gt_username = %s;'
    data = (username)

    cur.execute(cmd, data)

    profile = list(cur.fetchone())

    if profile[0]:
        cmd = 'SELECT * FROM classes WHERE instructor_gt_username = %s;'
        data = (username)
        cur.execute(cmd, data)
        classes = cur.fetchall()
    else:
        cmd = 'SELECT * FROM classes WHERE class_id in (SELECT class_id FROM roster WHERE gt_username = %s);'
        data = (username)
        cur.execute(cmd, data)
        classes = cur.fetchall()

    cur.close()
    conn.close()
    return profile, [list(x) for x in classes]


def create_class(class_name, semester, instructor_username, max_team_size=5):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'INSERT INTO classes (class_name, class_semester, instructor_gt_username, max_team_size) VALUES (%s, %s, %s, %s);'
    data = (class_name, semester, instructor_username, max_team_size)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def get_all_team_in_class(class_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()
    
    cmd = 'SELECT * FROM teams WHERE class_id = %s GROUP BY team_id'
    cur.execute(cmd,data)
    conn.commit()
    
    cur.close()
    conn.close()
    
def create_team(class_id, gt_username, team_name):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'INSERT INTO teams (class_id, gt_username, team_name, is_captain) VALUES (%s, %s, %s, %s);'
    data = (class_id, gt_username, team_name, True)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def add_to_team(class_id, gt_username, team_name):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()
    
    cmd = 'SELECT max_team_size FROM classes WHERE class_id = %s;'
    data = (class_id,)
    cur.execute(cmd, data)
    max_size = int(cur.fetchone()[0])

    cmd = 'SELECT gt_username FROM teams WHERE class_id = %s AND team_name = %s;'
    data = (class_id, team_name)
    cur.execute(cmd, data)
    cur_size = len(cur.fetchall()) 

    if cur_size == max_size:
        raise Exception('Cannot add more team members because the limit is reached')

    cmd = 'INSERT INTO teams (class_id, gt_username, team_name, is_captain) VALUES (%s, %s, %s, %s);'
    data = (class_id, gt_username, team_name, False)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def remove_from_team(team_id, gt_username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'DELETE FROM teams WHERE team_id = %s AND gt_username = %s;'
    data = (team_id, gt_username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def assign_team_captain(team_id, gt_username):
    conn = psycopg2.connect(**db)
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
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'UPDATE users SET comment = %s WHERE gt_username = %s;'
    data = (comment, username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

    
def get_user_comment(username):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'SELECT comment from users WHERE gt_username = %s;'
    data = (username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()
    
    
def enroll_student(username, class_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'INSERT INTO rosters (class_id, gt_username) VALUES (%s, %s);'
    data = (class_id, username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()
    
def unenroll_student(username, class_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'DELETE FROM rosters WHERE class_id = %s AND gt_username = %s  );'
    data = (class_id, username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def get_professor_classes(username):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'SELECT class_id FROM classes WHERE gt_username = %s  );'
    data = (username)
    
    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def get_all_student_usernames():
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT gt_username FROM users WHERE is_instructor = FALSE'
    cur.execute(cmd)

    student_usernames = [x[0] for x in cur.fetchall()]

    cur.close()
    conn.close()

    return student_usernames

def get_all_professor_usernames():
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cmd = 'SELECT gt_username FROM users WHERE is_instructor = TRUE'
    cur.execute(cmd)
    professor_usernames = [x[0] for x in cur.fetchall()]
    cur.close()
    conn.close()
    return professor_usernames

def register_user(username, is_instructor, email, first_name, last_name):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'INSERT INTO users (gt_username, is_instructor, email, first_name, last_name, comment) VALUES (%s, %s, %s, %s, %s, %s);'
    data = (username, is_instructor, email, first_name, last_name, '')

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def mass_register_users(userlist):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'INSERT INTO users (gt_username, is_instructor, email, first_name, last_name, comment) VALUES ' + '(%s, %s, %s, %s, %s, %s), '*(len(userlist)//6-1) + '(%s, %s, %s, %s, %s, %s);'
    cur.execute(cmd, userlist)
    conn.commit()

    cur.close()
    conn.close()

def enroll_from_roster(students, class_id):
    conn = psycopg2.connect(**db)
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