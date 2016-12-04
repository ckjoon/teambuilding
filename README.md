# Team 17: Team Building Application
Team Building Application for Junior Design

## Release Notes
Features:
* Professors are able to:
    * create classes 
    * import roster files from T-Square in .XLS format (see the UI issue workaround in the "Known Issues" section).
    * edit imported rosters (add/remove students)
    * switch between different classes they are teaching
    * see teams, their captains, who is in teams, etc.
* Students are able to:
    * leave relevant information in the comment section of their profile, such as previous experience, programming languages, what kind of team they iare looking for, etc.
    * switch between classes they are in that utilize our service
    * create teams (adding/removing students up to the limi)
    * send requests to join existing teams
        * in cases when a student sends requests to join multiple teams, as soon as one of the requests gets accepted, the rest of the requests will be deleted from the database
    * leave teams
    * if team captain:
        * approve and deny requests to join your team
        * transfer the team captain role to another team member
    
    
Known Issues:
* CAS login. 
    * Currently, users can log in using their username only (which is why this should not be used in production until CAS login is integrated). We wrote code that deals with all of that using CAS documentation for their API, but since we haven't received the permit from CAS yet, the code doesn't work. 
* Uploading rosters doesn't work properly through the UI.
    * We created a temporary workaround. You need to create a folder in the root called `rosters/`, put your .XLS roster files imported from T-Square in it, edit filename parameters in `roster_processor.py`, and then it as a python script.
* Generating final rosters (i.e., auto-matching) is not implemented.
* Input validation.
    * Weak, which leaves the service in its current somewhat vulnerable.

## Installation Guide
Ensure that you are using python 3 as well as pip3 and have virtualenv configured
to work with these versions.

CD into the repository and create a virtual environment using `virtualenv env`.
Then run the command `source env/bin/activate` (the two commands above are dependent on your OS and terminal application) to move into your virtual environment.
Install all the dependencies using `pip install -r requirements.txt`.
Use `deactivate` to exit the virtual environment when exiting the project directory.

Download and install [PostgreSQL](https://www.postgresql.org/download/), either locally or on a remote machine or host it using something like AWS or Azure.

Once you have installed PostgreSQL, create a file in `teambuilding/` called `config.py` and populate using the following parameters:
```
db = {
    'database': 'your_db_name',
    'user': 'your_db_username',
    'password': 'your_db_password',
    'host': 'your_db_host_address',
    'port': 'your_db_port'
}
UPLOAD_FOLDER = 'uploads/'#path for uploaded files
ALLOWED_EXTENSIONS = set(['csv'])#do not change this
```


We have also created a script that will set up the appropriate tables that the project utilizes. The script can be found in `teambuildingapp/db_setup.py` and ran using python3 (note that `config.py` setup is a must before running the script).

Start the server by running `runserver.py` as a python file.
