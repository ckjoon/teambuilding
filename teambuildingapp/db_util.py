import psycopg2
from teambuildingapp.config import *

def get_user_info(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT is_instructor, email, first_name, last_name, comment FROM users WHERE gt_username = \'%s\';'
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

def get_all_teams_in_class(class_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()
    
    cmd = ('SELECT team_name, username, emails, countUsers, teamid '
          'FROM ((SELECT team_name, team_id as teamid, COUNT(gt_username) '
          'as countUsers FROM teams where class_id = %s GROUP BY team_id, team_name ) t1 '
          ' INNER JOIN '
          '(SELECT team_id, gt_username as username FROM teams WHERE is_captain = True GROUP BY team_id, gt_username) t2 '
          'on teamid = t2.team_id) query1 inner join (select gt_username, email as emails from users) query2 on username = query2.gt_username;')
    data = (class_id,)
    print(cmd)
    print(cur.mogrify(cmd, data))

    cur.execute(cmd,data)
    
    all_teams = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return  all_teams
    
def create_team(class_id, gt_username, team_name):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'INSERT INTO teams (class_id, gt_username, team_name, is_captain) VALUES (%s, %s, %s, %s);'
    data = (class_id, gt_username, team_name, True)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def add_to_team(class_id, team_id, gt_username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()
    
    cmd = 'SELECT max_team_size FROM classes WHERE class_id = %s;'
    data = (class_id,)
    cur.execute(cmd, data)
    max_size = int(cur.fetchone()[0])

    cmd = 'SELECT gt_username FROM teams WHERE class_id = %s AND team_id = %s;'
    data = (class_id, team_id)
    cur.execute(cmd, data)
    cur_size = len(cur.fetchall()) 

    team_name = get_team_name(class_id, team_id)

    if cur_size == max_size:
        raise Exception('Cannot add more team members because the limit is reached')

    cmd = 'INSERT INTO teams (team_id, class_id, gt_username, team_name, is_captain) VALUES (%s, %s, %s, %s, %s);'
    data = (team_id, class_id, gt_username, team_name, False)
    print(cur.mogrify(cmd, data))

    remove_from_requests(class_id, team_id, gt_username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def add_team_request(class_id, team_id, gt_username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'INSERT INTO requests (class_id, team_id, gt_username) VALUES (%s, %s, %s)'
    data = (class_id, team_id, gt_username)

    cur.execute(cmd, data)
    conn.commit()
    cur.close()
    conn.close()

def remove_from_requests(class_id, team_id, gt_username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'DELETE FROM requests WHERE class_id = %s AND team_id = %s AND gt_username = %s;'
    data = (class_id, team_id, gt_username)

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
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT comment from users WHERE gt_username = %s;'
    data = (username,)
    #print(cur.mogrify(cmd, data))
    cur.execute(cmd, data)
    conn.commit()

    comment =  cur.fetchone()

    cur.close()
    conn.close()

    return comment[0]
    
def get_team_captain(class_id, team_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT gt_username from teams WHERE class_id = %s AND team_id = %s AND is_captain = TRUE;'
    data = (class_id, team_id)
    
    cur.execute(cmd, data)
    conn.commit()

    team_captain =  str(cur.fetchone()[0])

    cur.close()
    conn.close()

    return team_captain
    
def get_student_name(gt_username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT first_name, last_name from users WHERE gt_username = %s;'
    data = (gt_username,)
    print(cur.mogrify(cmd, data))
    cur.execute(cmd, data)
    conn.commit()

    name =  cur.fetchone()
    print(name)

    cur.close()
    conn.close()

    return name


def get_student_info(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT first from teams WHERE class_id = %s AND team_id = %s AND is_captain = TRUE;'
    data = (username,)
    #print(cur.mogrify(cmd, data))

    cur.execute(cmd, data)
    conn.commit()

    team_captain =  cur.fetchone()

    cur.close()
    conn.close()

    return team_captain[0]

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
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'DELETE FROM rosters WHERE class_id = %s AND gt_username = %s);'
    data = (class_id, username)

    cur.execute(cmd, data)
    conn.commit()

    cur.close()
    conn.close()

def get_professor_class_ids(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT class_id FROM classes WHERE instructor_gt_username = %s;'
    data = (username,)
    
    cur.execute(cmd, data)

    classes = [x[0] for x in cur.fetchall()]

    cur.close()
    conn.close()
    
    return classes

def get_professor_classes(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT class_id, class_name, class_semester, max_team_size FROM classes WHERE instructor_gt_username = %s;'
    data = (username,)
    
    cur.execute(cmd, data)

    classes = cur.fetchall()

    cur.close()
    conn.close()
    
    return classes

def get_all_students_in_team(class_id, team_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT gt_username, first_name, last_name, email FROM users WHERE gt_username in (SELECT gt_username from teams where class_id = %s AND team_id = %s);'
    data = (class_id, team_id)
    print(cur.mogrify(cmd, data))

    cur.execute(cmd, data)

    students_in_team = cur.fetchall()

    cur.close()
    conn.close()

    return students_in_team

def get_all_students_request(class_id, team_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT gt_username, first_name, last_name, email FROM users WHERE gt_username in (SELECT gt_username from requests where class_id = %s AND team_id = %s);'
    data = (class_id, team_id)
    print(cur.mogrify(cmd, data))

    cur.execute(cmd, data)

    requests = cur.fetchall()

    cur.close()
    conn.close()

    return requests


def get_all_student_usernames():
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT gt_username FROM users WHERE is_instructor = FALSE;'
    
    cur.execute(cmd)

    student_usernames = [x[0] for x in cur.fetchall()]

    cur.close()
    conn.close()

    return student_usernames

def get_team_name(class_id, team_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT team_name FROM teams WHERE class_id = %s AND team_id = %s;'
    data = (class_id, team_id)
    cur.execute(cmd, data)

    team_name = cur.fetchone()[0]

    cur.close()
    conn.close()

    return team_name

def get_all_professor_usernames():
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT gt_username FROM users WHERE is_instructor = TRUE;'
    
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
    print(userlist)
    cmd = 'INSERT INTO users (gt_username, is_instructor, email, first_name, last_name, comment) VALUES ' + '(%s, %s, %s, %s, %s, %s), '*(len(userlist)//6-1) + '(%s, %s, %s, %s, %s, %s);'
    cur.execute(cmd, userlist)
    conn.commit()

    cur.close()
    conn.close()

def get_student_enrolled_classnames(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT class_name from classes where class_id in (SELECT class_id from rosters WHERE gt_username = %s);'
    data = (username,)

    cur.execute(cmd, data)

    class_names =  [x[0] for x in cur.fetchall()]

    cur.close()
    conn.close()
    
    return class_names

def get_student_enrolled_classes(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT class_name, class_id from classes where class_id in (SELECT class_id from rosters WHERE gt_username = %s);'
    data = (username,)

    cur.execute(cmd, data)

    class_names = cur.fetchall()

    cur.close()
    conn.close()
    
    return class_names



def get_student_enrolled_class_id(username):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT class_id from classes where class_id in (SELECT class_id from rosters WHERE gt_username = %s);'
    data = (username,)

    cur.execute(cmd, data)

    class_names = [x[0] for x in cur.fetchall()]

    cur.close()
    conn.close()
    
    return class_names

def get_student_enrolled_team_id(gt_username, class_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT team_id from teams where class_id = %s AND gt_username = %s;'
    data = (class_id, gt_username)

    cur.execute(cmd, data)

    team_id = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return team_id

def get_class_max_team_size(class_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    cmd = 'SELECT max_team_size from classes where class_id = %s;'
    data = (class_id,)

    cur.execute(cmd, data)

    class_max = cur.fetchone()[0]
    print('debug'+str(class_max))
    cur.close()
    conn.close()
    
    return class_max



def enroll_from_roster(students, class_id):
    conn = psycopg2.connect(**db)
    cur = conn.cursor()

    registered_students = get_all_student_usernames()
    print (registered_students)
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