# Team 17: Team Building Application
Team Building Application for Junior Design

## Release Notes
New Features:
    1. Professors can upload the class roster and see all the created teams with their availability and their team manager. \n
    2. Students can edit their profiles and search for available teams with easy UI design.
Bug Fixed:
    1. Bug fixed in where professors were not able to see the availability of the teams on their dashboard (FIXED).
    2. Students were not able to see their updated profiles (FIXED).
    3. "Send Request" button was not responsive with the database (FIXED).
Known Bugs:
    1. Signout feature does not actually log out the user. It goes back to the signin html directly.
    2. Leaving team as the team manager deletes the team entirely. 
    
## Install Guide
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
db = {
    'database': 'teambuilding',
    'user': 'postgres',
    'password': '12345', # CHANGE THIS!
    'host': '111.111.111.111',
    'port': '1111'
}
```

Start the server with `python3 runserver.py`
