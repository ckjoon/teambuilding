from teambuildingapp import app
from flask import render_template, request, url_for, redirect, session, make_response
from flask_cas import login_required

from teambuildingapp.db_util import *


@app.route("/")
def main():
    return render_template('signin.html')

@app.route("/prof_home")
# Uncomment this to require CAS to access this page
# @login_required
def prof_home():
    #profile, classes = db_util.get_user_info()
    # return render_template('prof_home.html', classes)
    return render_template('prof_home.html')

@app.route("/student_home")
# Uncomment this to require CAS to access this page
# @login_required
def student_home():
    firsttime = request.cookies.get('firsttime')
    #username = request.cookies.get('username')
    username = session['username']
    class_id = session['class_id']
    print(username)
    student_comment = get_user_comment(username)
    student_enrolled_classes = get_student_enrolled_classnames(username)
    teamsize = get_class_max_team_size(class_id)
    all_teams = get_all_teams_in_class(class_id)
    print(student_comment)
    print(student_enrolled_classes)
    print(all_teams)
    resp = make_response(render_template('student_home.html',comment = student_comment, max_team_size = teamsize, classes = student_enrolled_classes, teams = all_teams));
    resp.set_cookie('firsttime', '', expires=0)
    return resp

@app.route("/signin_error")
def signin_error():
    return render_template('signin_error.html')

@app.route("/team_manager_panel")
def team_manager_panel():
    return render_template('team_manager_panel.html',)

@app.route("/api/login", methods=['POST'])
def login():
    #handle login stuff.
    if request.method == 'POST':
        gtusername = request.form.get('gtusername')
        # password = request.form.get('password')
        all_students = get_all_student_usernames()
        all_professors = get_all_professor_usernames()
        student_class_ids = get_student_enrolled_class_id(gtusername)
        prof_class_ids = get_professor_classes(gtusername)
        

        print(student_class_ids)
        #print(all_professors)
        
        #print(gtusername)
        #print(all_students)
        #for s in all_students:
            #print(s)
        is_student = True
        if gtusername in all_students:
            session['username'] = gtusername
            session['firsttime'] = True
            session['class_id'] = student_class_ids[0]
            team_id = get_student_enrolled_team_id(session['username'], session['class_id'])
            session['team_id'] = team_id  
        elif gtusername in all_professors:
            is_student = False
            session['username'] = gtusername
            session['firsttime'] = True
            session['class_id'] = prof_class_ids[0]
        else:
            return redirect(url_for('signin_error'))
        # check if they exist
        if session['team_id']:
            resp = make_response(redirect(url_for('team_manager_panel')))
            return resp
        if is_student:
            resp = make_response(redirect(url_for('student_home')))
            resp.set_cookie('firsttime', 'true')
            return resp
        else:
            return redirect(url_for('prof_home'))
        

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