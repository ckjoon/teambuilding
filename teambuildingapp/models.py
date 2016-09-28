from teambuildingapp import app
from flask_sqlalchemy import Model, Column, Integer, String

# Represents a user. User is related to a team by it's team ID'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    team_id = db.Column(db.Integer)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# Represents a Team
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(120), unique=True)
    team_leader = db.Column(db.Integer, unique=True)

    def __init__(self, team_name, team_leader):
        self.team_name = team_name
        self.team_leader = team_leader

    def __repr__(self):
        return '<User %r>' % self.team_name


# class Roster(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    # put some stuff about rosters here