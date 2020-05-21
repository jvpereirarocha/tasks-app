from flask import Flask
from config import Production, Develop, Testing
from .extensions import db, migrate


def create_app(environment='Production'):
    app = Flask(__name__, instance_relative_config=True)
    if environment == 'Production' or environment == 'production':
        app.config.from_object(Production)
    elif environment == 'Develop' or environment == 'develop':
        app.config.from_object(Develop)
    elif environment == 'Testing' or environment == 'testing':
        app.config.from_object(Testing)
    else:
        raise ValueError('Invalid parameter')

    db.init_app(app)

    init_migrate(app, db)

    routers(app)

    return app


def init_migrate(app, db):
    migrate.init_app(app, db)


def routers(app):
    from .views import bp
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='index')
