import os
from flask import Flask, request, render_template, jsonify, redirect, url_for, make_response
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
# from flask_cors import CORS, cross_origin
import json
# import os
import cdacrud
import registration
# from werkzeug import secure_filename
import uuid
from flask import make_response
from functools import wraps, update_wrapper
import datetime
from urlparse import urlparse
from flask_cache import Cache
import requests

app = Flask(__name__,static_url_path='')
application = app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "onboardingpage"


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)

@login_manager.user_loader
def user_loader(id):
        user=registration.user_loader(id)
        return user

@login_manager.unauthorized_handler
@nocache
def unauthorized_handler():
    return redirect('/',code=302)

@app.route('/')
def onboardingpage():
    return render_template('login.html',error='')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',error='')

@app.route('/signup')
# #@cross_origin()
def register():
    return render_template('signup.html', error='')

@app.route('/register', methods=["POST"])
#@cross_origin()
def register_user():
    print request.form
    return registration.registeruser(request.form)

@app.route('/authenticate', methods=['POST'])
#@cross_origin()
def loginauthorisation():
    print request.form
    #remember = request.form.getlist('remember')
    user = registration.authenticateuser(request.form)
    print user
    if user == None:
        return render_template('login.html', error='Invalid credentials. Please enter correct details.')
    elif isinstance(user, unicode) != True:
        login_user(user)
        cdacrud.log_activity(user,'logged in')
        return redirect(url_for('api_interface'))

@app.route("/api/userData")
@login_required
def userData():
    return cdacrud.getUserData(current_user)

@app.route("/api/updateKey")
@login_required
def updateKey():
    return cdacrud.updateKey(current_user)

@app.route('/apiinterface')
#@cross_origin()
@login_required
def api_interface():
    return render_template('api_interface.html',editorname=current_user.userid)
    # return current_user.email

app.config['SECRET_KEY'] = 'srkYSIQSMT21Rjs8'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)