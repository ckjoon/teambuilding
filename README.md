# teambuilding
Team Building Application for Junior Design

## Build and run
Ensure that you are using python 3 as well as pip3 and have virtualenv configured
to work with these versions.

CD into the repository and create a virtual environment using `virtualenv env`. 
Then run the command `source env/bin/activate` to move into your virtual environment.
Install all the dependencies using `pip3 install -r requirements.txt`.
Use `deactivate` to exit the virtual environment when exiting the project directory.

Download and install PostgreSQL. There is a nice article you can follow that will walk you through
these steps [here](http://killtheyak.com/use-postgresql-with-django-flask/). It is suggested for OSX
users to use Postgres.app. 

Once you have installed Postgres initialize the database with the name 'teambuilding'.
Create a file in the base directory of the project named 'config.py'.

`touch config.py`

Inside config.py add the following properties:

```
    SQLALCHEMY_DATABASE_URI = "postgresql://yourusername:yourpassword@localhost/teambuilding"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CAS_SERVER = 'https://login.gatech.edu/cas/serviceValidate'
    CAS_AFTER_LOGIN  = 'student_home' # CHANGE THIS: needs to redirect to somehow determine
                                      # what kind of person is logging in.
    #CAS_ATTRIBUTES_SESSION_KEY = 'supersecretsessionkey' #set your own unique session key here
    SECRET_KEY = 'supersecretsessionkey' #set your own unique session key here
```

Start the server with `python3 runserver.py`