from teambuildingapp import app
from flask import render_template, request, url_for, redirect, session, make_response
from flask_cas import login_required

from teambuildingapp.db_util import update_user_comment, get_all_student_usernames


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
    resp = make_response(render_template('student_home.html'))
    # resp.set_cookie('firsttime', '', expires=0)
    return resp

@app.route("/signin_error")
def signin_error():
    return render_template('signin_error.html')

@app.route("/team_manager_panel")
def team_manager_panel():
    return render_template('team_manager_panel.html')

@app.route("/api/login", methods=['POST'])
def login():
    #handle login stuff.
    if request.method == 'POST':
        gtusername = request.form.get('gtusername')
        # password = request.form.get('password')

        all_students = get_all_student_usernames()
        print(gtusername)
        print(all_students)
        for s in all_students:
            print(s)

        if gtusername in all_students:
            session['username'] = gtusername
            session['firsttime'] = True
        else:
            return redirect(url_for('signin_error'))
        # check if they exist
        if gtusername != "jchoi302":
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
