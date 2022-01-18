from flask import Blueprint, render_template, abort, Response, redirect, url_for
from flask_login import login_required, current_user

from ..db import db
from ..forms import CreationNoteForm, UpdatedNoteForm
from ..models import Note

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')


@notes_bp.route('/')
@login_required
def list() -> str:
    notes = Note.query.all()
    return render_template('notes/list.html', notes=notes)


@notes_bp.route('/<int:note_id>')
@login_required
def index(note_id: int) -> str:
    note = Note.query.get(note_id)
    if not note:
        abort(404, 'Note doesnt exist!')
    return render_template('notes/index.html', note=note)


@notes_bp.route('/update/<int:note_id>', methods=['GET', 'POST'])
@login_required
def update(note_id: int) -> Response or str:
    note = Note.query.get(note_id)
    if not note:
        abort(404, 'Note doesnt exist!')
    form = UpdatedNoteForm(obj=note)

    if form.validate_on_submit():
        form.populate_obj(note)
        db.session.commit()
        return redirect(url_for('notes.index', note_id=note.id))
    return render_template('notes/update.html', form=form)


@notes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create() -> Response or str:
    form = CreationNoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data,
                    description=form.description.data,
                    user=current_user)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('notes.list'))
    return render_template('notes/create.html', form=form)
