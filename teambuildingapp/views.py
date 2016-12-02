from teambuildingapp import app
from flask import render_template, request, url_for, redirect, session, make_response
from flask_cas import login_required
#from roster_processor import process_roster

from teambuildingapp.db_util import *


@app.route("/")
def main():
    return render_template('signin.html')

@app.route("/logout")
def logout():
    session.clear()

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    class_name = request.form.get('coursename')
    semester = request.form.get('semester')
    teamsize = request.form.get('teamsize')
    if file and allowed_file(file.filename):

        filename = file.filename

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        create_class(class_name, semester, session['username'], teamsize)
        process_roster(filename)
        return redirect(url_for('student_home'))
        

@app.route("/prof_home")
# Uncomment this to require CAS to access this page
# @login_required
def prof_home():
    username = session['username']
    #profile, classes = db_util.get_user_info()
    # return render_template('prof_home.html', classes)
    if 'last_class' not in session:
        classes = get_professor_classes(username)
        if len(classes) > 0:
            session['last_class'] = (classes[0][0], '{0} ({1})'.format(classes[0][1], classes[0][2]))
            session['max_team_size'] = classes[0][3]
            session['class_names'] = ['{0} ({1})'.format(x[1], x[2]) for x in classes]
            session['teams'] = get_all_teams_in_class(session['last_class'][0])
            
        else:
            session['last_class'] = None
            session['max_team_size'] = None
            session['class_names'] = []
            session['teams'] = []
    return make_response(render_template('prof_home.html', last_class=session['last_class'], max_team_size=session['max_team_size'], classes=session['class_names'], teams=session['teams']))

@app.route("/student_home")
# Uncomment this to require CAS to access this page
# @login_required
def student_home():
    #firsttime = request.cookies.get('firsttime')
    #username = request.cookies.get('username')
    username = session['username']
    #print(username)
    if 'class_id' not in session:
        student_class_ids = get_student_enrolled_class_id(username)
        if len(student_class_ids) > 0:
            session['class_id'] = student_class_ids[0]
            student_enrolled_classes = get_student_enrolled_classnames(username)
            teamsize = get_class_max_team_size(session['class_id'])
            all_teams = get_all_teams_in_class(session['class_id'])
        else:
            session['class_id'] = None
    else:
        teamsize = get_class_max_team_size(session['class_id'])
        all_teams = get_all_teams_in_class(session['class_id'])
    
    student_comment = get_user_comment(username)
    student_enrolled_classes = get_student_enrolled_classes(username)
    #print(student_comment)
    #print(student_enrolled_classes)
    #print(all_teams)
    resp = make_response(render_template('student_home.html',
                        comment = student_comment, max_team_size = teamsize, 
                        classes = student_enrolled_classes, teams = all_teams))
    #resp.set_cookie('firsttime', '', expires=0)
    return resp

@app.route("/signin_error")
def signin_error():
    return render_template('signin_error.html')

@app.route("/team_manager_panel")
def team_manager_panel():
    team_id = session['team_id']
    class_id = session['class_id']
    team_name = get_team_name(class_id, team_id)
    team_captain = get_team_captain(class_id, team_id)
    team_captain_name = get_student_name(team_captain)
    user_captain = False
    students = get_all_students_in_team(class_id, team_id)
    requests = get_all_students_request(class_id, team_id)

    if session['username'] == team_captain:
        user_captain = True  
    
    resp = make_response( 
        render_template('team_manager_panel.html', 
                        team_name = team_name, team_captain_name = team_captain_name, 
                        user_captain = user_captain, students_in_team = students,
                         current_user = session['username'], requests = requests ))
    return resp

@app.route("/api/login", methods=['POST'])
def login():
    #handle login stuff.
    if request.method == 'POST':
        gtusername = request.form.get('gtusername')
        # password = request.form.get('password')
        all_students = get_all_student_usernames()
        all_professors = get_all_professor_usernames()

        #print(student_class_ids)
        #print(all_professors)
        #print(gtusername)
        #print(all_students)
        #for s in all_students:
            #print(s)
        is_student = True
        if gtusername in all_students:
            student_class_ids = get_student_enrolled_class_id(gtusername)
            session['username'] = gtusername
            #session['firsttime'] = True
            if len(student_class_ids) > 0:
                session['class_id'] = student_class_ids[0]
                team_id = get_student_enrolled_team_id(session['username'], session['class_id'])
                session['team_id'] = team_id
                if session['team_id'] != None:
                    resp = make_response(redirect(url_for('team_manager_panel')))
                else:
                    resp = make_response(redirect(url_for('student_home')))
            else:
                session['class_id'] = None
                session['team_id'] = None
        
        elif gtusername in all_professors:
            #prof_class_ids = get_professor_classes(gtusername)
            is_student = False
            session['username'] = gtusername
            #session['firsttime'] = True

            resp = make_response(redirect(url_for('prof_home')))
        else:
            return redirect(url_for('signin_error'))
        return resp
        

@app.route("/updateIntroduction", methods=['POST'])
def updateIntroduction():
    if request.method == 'POST':
        text = request.form.get('introtext')
        update_user_comment(session['username'], text)
        return redirect(url_for('student_home'))

@app.route("/createTeam", methods=['POST'])
def createTeam():
    if request.method == 'POST':
        text = request.form.get('team_name')
        print(text)
        create_team(session['class_id'],session['username'], text)
        return redirect(url_for('student_home'))

@app.route("/acceptdecline", methods=['POST'])
def accept_decline():
    if request.method == 'POST':
        text = request.form.get('gt_username')
        print(text)
        if (request.form['submit']=='Accept'):
            add_to_team(session['class_id'], session['team_id'], text)

        if (request.form['submit']=='Decline'):
            remove_from_requests(session['class_id'], session['team_id'], text)

        remove_from_requests(session['class_id'], session['team_id'], session['username'])
        return redirect(url_for('team_manager_panel'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/requestTeam", methods=['POST'])
def requestTeam():
    if request.method == 'POST':
        team_id = request.form.get('team_id')
        add_team_request(session['class_id'], team_id, session['username'])

        return redirect(url_for('student_home'))


@app.route("/chooseClass", methods=['POST'])
def choose_classs():
    if request.method == 'POST':
        class_id = request.form.get('class')
        print(class_id)
        session['class_id'] = class_id
        return redirect(url_for('student_home'))