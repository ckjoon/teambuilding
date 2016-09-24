from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('signin.html')

@app.route("/prof_home")
def prof_home():
    return render_template('prof_home.html')

@app.route("/student_home")
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
