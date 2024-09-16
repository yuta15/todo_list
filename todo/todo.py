from datetime import datetime
import sqlite3

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

# このファイルはTODO部分を作成するためのファイルです。
# BluePrintを使用して作成しており、__init__.pyにて読み込むことで使用しています。

bp = Blueprint('todo', __name__)


def varificate_form(**unverified_form):
    """
    formに入力されたデータが正しいデータ形式か確認する。
    title:str
    body:str
    end_time:str
    is_completed:int
    """
    verified_form = {
            'title': None,
            'body': None,
            'end_time': None,
            'is_completed': None,
            'form_error': None
    }
    try:
        verified_form['title'] = unverified_form.get('title')
        verified_form['body'] = unverified_form.get('body')
        verified_form['end_time'] = datetime.fromisoformat(unverified_form.get('end_time'))
        verified_form['is_completed'] = 1 if unverified_form.get('is_completed') is not None else 0

        if verified_form['title'] is None or verified_form['body'] is None or verified_form['end_time'] is None:
            verified_form['form_error'] = 'Title, body, end_time is required'
            return verified_form

        elif not isinstance(verified_form['title'], str) or not isinstance(verified_form['body'], str) or not isinstance(verified_form['end_time'], datetime):
            verified_form['form_error'] = 'Form Parmeter is Required'
            return verified_form

    except:
        verified_form['form_error'] = 'Unknown Error'
        return verified_form

    else:
        return verified_form


@bp.route('/')
def index():
    """
    未完了のタスク一覧を表示
    
    """
    db = get_db()
    todos = []
    for todo in db.execute('SELECT * FROM todo WHERE is_completed = 0;').fetchall():
        todos.append(dict(todo))
    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    """
    新規タスクを作成する。
    
    """
    if request.method == 'POST':
        verified_form = varificate_form(**dict(request.form))
        if verified_form['form_error'] is not None:
            abort(400)
        else:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO todo (title, body, end_time)'
                    ' VALUES (?, ?, ?);',
                    (verified_form['title'], verified_form['body'], verified_form['end_time'])
                )
                db.commit()
            except (sqlite3.DataError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
                flash(e)
                abort(500)
            else: 
                return redirect(url_for('todo.index'),  code=303)
    return render_template('todo/create.html'),200


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    """
    特定のTODOを変更する。
    arg:
        id:TODOのID
    """
    db = get_db()
    todo = db.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        verified_form = varificate_form(**dict(request.form))
        print(verified_form)
        if verified_form['form_error'] is not None:
            abort(400)
        else:
            try:
                db = get_db()
                db.execute( 
                    'UPDATE todo SET title = ?, body = ?, end_time = ?, is_completed = ? WHERE id = ?;', 
                    (verified_form['title'], verified_form['body'], verified_form['end_time'], verified_form['is_completed'], id)
                )
                db.commit()
            except (sqlite3.DataError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
                flash(e)
                abort(400)
            else:
                return redirect(url_for('todo.index'), 303)
    return render_template('todo/edit.html', todo=todo)


@bp.route('/<int:id>/delete', methods=('GET', 'POST',))
def delete(id):
    """
    タスクを削除する。
    arg:
        id:TODOのID
    """
    db = get_db()
    delete_todo = db.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone()
    if delete_todo is None:
        abort(400)
    if request.method == 'POST':
        try:
            db.execute(
                'DELETE FROM todo WHERE id = ?;',(id,)
            )
            db.commit()
        except (sqlite3.DataError, sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            flash(e)
            return redirect(url_for('/'))
        else:
            return redirect(url_for('todo.index'),303)
    return render_template('todo/delete.html', todo=delete_todo)


@bp.route('/complete')
def complete():
    """
    完了済みタスク一覧を表示する。
    """
    db = get_db()
    todos = []
    for todo in db.execute('SELECT * FROM todo WHERE is_completed = 1;').fetchall():
        todos.append(dict(todo))
    return render_template('todo/complete.html', todos=todos)