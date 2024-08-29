from datetime import datetime

from flask import g
from flask import request
from flask import redirect
from flask import flash
from flask import Blueprint
from flask import render_template
from flask import session
from flask import url_for
from werkzeug.exceptions import abort

from todo.db import get_db


bp = Blueprint('todo', __name__)


def get_todo(id):
    db = get_db()
    todo = get_db().execute(
        'SELECT * FROM todo WHERE id = ?;',(id)
    ).fetchone()
    if todo is None:
        abort(404, f"Todo is Not Exists id:{id}")

    return dict(todo)


@bp.route('/')
def index():
    db = get_db()
    todos = []
    for todo in db.execute('SELECT * FROM todo WHERE is_state = 0;').fetchall():
        todos.append(dict(todo))

    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        end_time = request.form['end_time']
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'
        elif not end_time:
            error = 'Endtime is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO todo (title, body, end_time)'
                ' VALUES (?, ?, ?);',
                (title, body, datetime(end_time))
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    db = get_db()
    todo = db.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        end_time = datetime(request.form['end_time'])
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'
        elif not end_time:
            error = 'EndTime is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE todo SET title = ?, body = ?, end_time = ? WHERE id = ?;', 
                (title, body, end_time, id)
            )
        return redirect(url_for('todo.index'))

    return render_template('todo/edit.html', todo=todo)


@bp.route('/delete', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute(
        'DELETE FROM todo WHERE id = ?',(id)
    )
    db.commit()

    return redirect(url_for('todo.index'))


@bp.route('/complete')
def complete():
    db = get_db()
    todos = []
    for todo in db.execute('SELECT * FROM todo WHERE is_state = 1;').fetchall():
        todos.append(dict(todo))

    return render_template('todo/complete.html', todos=todos)