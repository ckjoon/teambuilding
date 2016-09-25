from teambuildingapp import app
from flask import render_template, request, url_for, redirect, session
from flask_cas import login_required

@app.route("/")
def main():
    return render_template('signin.html')

@app.route("/prof_home")
# Uncomment this to require CAS to access this page
# @login_required
def prof_home():
    return render_template('prof_home.html')

@app.route("/student_home")
# Uncomment this to require CAS to access this page
# @login_required
def student_home():
    return render_template('student_home.html')

@app.route("/api/login", methods=['POST'])
def login():
    #handle login stuff.
    if request.method == 'POST':
        if request.form.get('gtusername') != "jchoi302":
            return redirect(url_for('student_home'))
        else:
            return redirect(url_for('prof_home'))