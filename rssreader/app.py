#-*- coding: utf-8 -*-
from flask import Flask, Blueprint, redirect, url_for
from flask.ext.login import current_user

from .config import config
from .database import db
from .extensions import login_manager
from feed import feed_blueprint
from user import user_blueprint, User


__all__ = ['create_app']
main_blueprint = Blueprint('main', __name__)
blueprints = (main_blueprint, user_blueprint, feed_blueprint,)

@main_blueprint.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('feeds.list_entries'))
    return "Landing page"

def create_app():
    app = Flask(__name__) # FIXME: is it correct name?

    app.config.from_object(config)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    db.init()

    login_manager.login_view = 'user.login'
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    login_manager.init_app(app)

    return app
