from flask import Blueprint, render_template

error_bp = Blueprint('errors', __name__)


@error_bp.app_errorhandler(404)
def handle_404(err):
    return render_template('errors/404.html'), 404


@error_bp.app_errorhandler(500)
def handle_500(err):
    return render_template('errors/500.html'), 500
