from datetime import datetime, timedelta
from dateutil import tz
import time
from sqlalchemy import create_engine,or_,desc,asc,and_,func
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.orm.exc import NoResultFound
from models import Base,User,Logdetails,Documents
from flask import Flask, url_for, render_template, flash, abort,current_app,redirect,jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import json
import requests
from math import ceil
import re
import uuid
import string
import datetime
from sqlalchemy import Date, cast
import config

engine = create_engine('mysql://'+config.databasedetails['username']+':'+config.databasedetails['password']+'@'+config.databasedetails['hostname']+':'+config.databasedetails['port']+'/'+config.databasedetails['databasename'],pool_size=10,pool_pre_ping=True,pool_recycle=3600 , echo=False,connect_args={"charset":"utf8mb4"})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def getUserData(current_user):
    session=DBSession()
    user=session.query(User).filter_by(userid=current_user.userid).one()
    userdata = {}
    userdata["email"] = user.email
    userdata["apikey"] = user.api_key
    userdata["noofrequests"] = user.no_of_requests
    print userdata
    return jsonify(userdata)

def updateKey(current_user):
    session=DBSession()
    user=session.query(User).filter_by(userid=current_user.userid).one()
    user.api_key = uuid.uuid4()
    session.commit()
    print user
    return 'done'

def log_activity(currentuser,activity):
    session=DBSession()
    log=Logdetails(logid=uuid.uuid4(),userid=current_user.userid,activity=activity,logtime=datetime.datetime.now())
    session.add(log)
    session.commit()

def addcard(filename,data,current_user):
    print data
    session=DBSession()
    doc=Documents(docid=uuid.uuid4(),documentname=filename,documentholder=current_user.userid)
    session.add(doc)
    session.commit()
    session.close()
    return "hello"

def updaterequests(current_user):
    session = DBSession()
    user=session.query(User).filter_by(userid=current_user.userid).one()
    user.no_of_requests += 1
    session.commit()