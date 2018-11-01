from datetime import datetime, timedelta
from dateutil import tz
import time
from sqlalchemy import create_engine,or_,desc,asc,and_,func
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.orm.exc import NoResultFound
from models import Base,User,Logdetails
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

engine = create_engine('mysql://root:karthikkumar@localhost:3306/ocr',pool_size=10,pool_pre_ping=True,pool_recycle=3600 , echo=False,connect_args={"charset":"utf8mb4"})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def log_activity(currentuser,activity):
    session=DBSession()
    log=Logdetails(logid=uuid.uuid4(),userid=current_user.userid,activity=activity,logtime=datetime.datetime.now())
    session.add(log)
    session.commit()