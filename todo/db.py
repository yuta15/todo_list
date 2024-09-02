from datetime import datetime
import sqlite3

import click
from flask import current_app
from flask import g


def get_db():
    """
    db接続用の関数
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    """
    dbとのコネクションをクローズする関数。
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    dbの初期化を行う関数。
    """
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.executescript(f.read())
        db.commit()


@click.command('init-db')
def init_db_command():
    """
    db初期化する関数のコマンドを定義する関数
    """
    init_db()
    click.echo('Initialized the database')
    
    
def init_app(app):
    """
    dbクリーンアップ時の動作を指定
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)