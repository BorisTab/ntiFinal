import hashlib

from flask import abort
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template

from app.constants import salt

from app.extensions import db
from app.extensions import login_user
from app.extensions import current_user
from app.extensions import login_manager
from app.extensions import login_required

from app.ar_server.models.db_models import Users
from app.ar_server.models.forms.login_form import LoginForm
from app.ar_server.models.forms.registration_form import RegistrationForm

from app.ar_server.models.model_gatherer import ModelGatherer


blueprint = Blueprint('ar', 'ar')

login_manager.login_view = '/ar/login'


@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('ar.main'))
    elif request.method == 'POST':
        _login = login_form.data['email']
        password = login_form.data['password'].encode('utf-8')

        password = hashlib.sha256(password + salt).hexdigest()

        # ToDo: add frontend validation
        if login_form.validate():
            user = db.session.query(Users).filter_by(email=_login, password=password).first()

            try:
                if user.password == password:
                    login_user(user)
                    _next = request.args.get('next')

                    return redirect(_next or url_for('ar.main'))
            except Exception as e:
                print(e.with_traceback(e.__traceback__))
                return abort(401)

    return render_template('login.html', form=login_form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():

    register_form = RegistrationForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('ar.main'))

    elif request.method == 'POST':
        form_login = register_form.data['email']
        form_password = register_form.data['password'].encode('utf-8')

        # ToDo: add frontend validation
        if register_form.validate():
            try:
                new_user = Users(form_login, hashlib.sha256(form_password + salt).hexdigest())
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)
                _next = request.args.get('next')

                return redirect(_next or url_for('ar.main'))
            except Exception as e:
                print(e.with_traceback(e.__traceback__))
                # ToDo: user exists
                return abort(401)
    return render_template('register.html', form=register_form)


@login_manager.user_loader
def load_user(_login):
    return Users.query.filter_by(email=_login).first()


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def main():
    return render_template('ar.html')


@blueprint.route('/get_model', methods=['POST'])
def get_model():
    max_lat = round(float(request.form['right-up-lat']), 2)
    max_lon = round(float(request.form['right-up-lng']), 2)
    min_lat = round(float(request.form['left-bottom-lat']), 2)
    min_lon = round(float(request.form['left-bottom-lng']), 2)

    gatherer = ModelGatherer()
    gatherer.get_model(max_lat, max_lon, min_lat, min_lon)

    return '200'


@blueprint.route('/put', methods=['GET'])
def put_file():
    pass


########################
#        DANGER        #
#    DEBUG USE ONLY    #
########################


@blueprint.route('/create')
def create_db():
    db.create_all()
    db.session.commit()
    return '200'


@blueprint.route('/drop')
def drop_db():
    db.drop_all()
    db.session.commit()
    return '200'
