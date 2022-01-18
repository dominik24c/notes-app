from flask import Blueprint, render_template, Response

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index() -> str or Response:
    return render_template('home/index.html')
