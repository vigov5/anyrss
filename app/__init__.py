from flask import Flask, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config.from_object('config')

auth = BasicAuth()
basic_auth = BasicAuth(app)

db = SQLAlchemy(app)

class AuthException(HTTPException):
    def __init__(self, message):
        # python 3
        super().__init__(message, Response(
            message, 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

from app import views, models  # nopep8

admin = Admin(app, url='/admin', template_mode='bootstrap3')
admin.add_view(models.SourceView(db.session, name='Sources'))

with app.app_context():
    db.create_all()