from flask import Flask, render_template, request, url_for, redirect
from flask_cas import CAS, login_required
app = Flask(__name__)
CAS(app, '/cas') # this adds the prefix '/api/cas/' to the /login and /logout
                      # routes that CAS provides
                      
app.config['CAS_SERVER'] = 'https://login.gatech.edu/cas/serviceValidate'
app.config['CAS_AFTER_LOGIN'] = 'student_home' # CHANGE THIS: needs to redirect to somehow determine
                                               # what kind of person is logging in.

@app.route("/")
def main():
    return render_template('signin.html')

@app.route("/prof_home")
@login_required
def prof_home():
    return render_template('prof_home.html')

@app.route("/student_home")
@login_required
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
    

if __name__ == "__main__":
    app.run()
