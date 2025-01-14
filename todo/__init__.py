import os

from flask import Flask


def create_app(test_config=None):
    """
    test_config
    
    """
    app = Flask(__name__)
    app.config.from_mapping(
        SECURITY_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'todo.sqlite'),
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    from . import todo
    app.register_blueprint(todo.bp)
    app.add_url_rule('/', endpoint='index')

    return app