'''example of 1 file flask application that uses an API and ORM'''

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# TODO make API request

# configuratinos for application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(app)


# routes for application
@app.route('/')
def root():
    api_request = requests.get('http://api.open-notify.org/astros.json')
    astro_data = api_request.json()
    num_astros = astro_data['number']
    return 'There are {} astros in space'.format(num_astros)

@app.route('/refresh')
def refresh():
    DB.drop_all()
    DB.create_all()
    api_request = requests.get('http://api.open-notify.org/astros.json')
    astro_data = api_request.json()
    num_astros = astro_data['number']
    record = Astronauts(num_astronauts=num_astros)
    DB.create_all()
    DB.session.add(record)
    DB.session.commit()
    return 'Database Updated! {}'.format(record)

@app.route("/iss-location")
def iss():
    api_request = requests.get("http://api.open-notify.org/iss-now.json")
    iss_location = api_request.json()
    position = iss_location["iss_position"]
    return "The ISS is here: (LO: {}, LA: {})".format(position["longitude"], position["latitude"])

class Astronauts(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    num_astronauts = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return 'number of astros: {}'.format(self.num_astronauts)