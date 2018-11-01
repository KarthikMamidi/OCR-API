import datetime
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.orm.exc import NoResultFound
from threading import Thread
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash,check_password_hash
from models import Base,User,Logdetails
import uuid
from flask import Flask, url_for, render_template, flash, abort,current_app,redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
import requests
import json

engine = create_engine('mysql://root:karthikkumar@localhost:3306/ocr',pool_size=10,pool_pre_ping=True,pool_recycle=3600 , echo=False,connect_args={"charset":"utf8mb4"})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def user_loader(id):
    session = DBSession()
    try:
        print id
        user = session.query(User).filter_by(userid=id).one()
        returnuser=user
        session.close()
        return user
    except NoResultFound:
        session.close()
        return None


def authenticateuser(loginformdata):  # loginverification
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=loginformdata['email']).one()
        print user
    except NoResultFound, e:
        session.close()
        return None
    try:
        if user.password:
            if check_password_hash(user.password,loginformdata['password']):
                returnuser=user
                session.close()
                return returnuser
            return None
        session.close()
        return None
    except Exception, e:
        session.close()
        return None

def registeruser(signupformdata):
    session = DBSession()
    user = User(email=signupformdata['email'], userid=uuid.uuid4(), password=generate_password_hash(signupformdata['password']), date_added=datetime.datetime.utcnow(), api_key=uuid.uuid4(), no_of_requests=0)
    session.add(user)
    session.commit()
    return render_template("registered.html", error='')