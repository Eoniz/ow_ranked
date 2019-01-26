from flask import Blueprint, render_template, redirect
from src import db

mod_prediction = Blueprint('prediction', __name__)

@mod_prediction.route('/')
def index():
    return render_template('prediction/index.html')