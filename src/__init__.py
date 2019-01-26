from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return redirect('/')

from src.mod_prediction.controller import mod_prediction
app.register_blueprint(mod_prediction)

db.create_all()