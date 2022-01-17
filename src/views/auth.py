from flask import Blueprint, render_template, \
    redirect, Response, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user

from ..db import db
from ..forms import LoginForm, RegistrationForm
from ..models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST', 'GET'])
def login() -> str or Response:
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify(form.password.data):
                login_user(user)
                return redirect(url_for('notes.index'))
            else:
                flash('Invalid credentials!', 'error')
        else:
            flash('Invalid username!', 'error')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=["GET", "POST"])
def register() -> str or Response:
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    first_name=form.first_name.data, last_name=form.last_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('auth.login'))
