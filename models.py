from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,VARCHAR, Text,Date, DateTime, ForeignKey, Boolean,UniqueConstraint
import mysql.connector

engine = create_engine('mysql://root:karthikkumar@localhost:3306/ocr', pool_pre_ping=True,echo=False,connect_args={"charset":"utf8mb4"})
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    email = Column(String(100))
    userid = Column(VARCHAR(36), primary_key=True)
    password = Column(String(256))
    date_added = Column(DateTime)
    api_key = Column(VARCHAR(36), primary_key=True)
    no_of_requests = Column(Integer)
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.userid

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class ApiKey(Base):
    __tablename__='apikey'
    userid=Column(VARCHAR(36),ForeignKey('user.userid'))
    apikey=Column(VARCHAR(36), primary_key=True)
    password=Column(String(256))

class Logdetails(Base):
    __tablename__='logdata'
    logid=Column(VARCHAR(36),primary_key=True)
    userid=Column(String(36),ForeignKey('user.userid'))
    activity=Column(String(256))
    logtime=Column(DateTime)

class Documents(Base):
    __tablename__ = 'docs'
    docid=Column(String(36),primary_key=True)
    documentname=Column(String(36),unique=True)
    documentholder=Column(String(36),ForeignKey('user.userid'))

if __name__ == "__main__": 
    conn = engine.connect()
    Base.metadata.create_all(engine)
    conn.close()
