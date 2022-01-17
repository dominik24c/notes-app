from flask import Blueprint
from flask_login import login_required

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')


@notes_bp.route('/')
@login_required
def index() -> str:
    return 'Note'
