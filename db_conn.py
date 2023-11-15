from sqlalchemy import create_engine, text, Integer, String, BigInteger, SmallInteger, Date
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from flask_login import UserMixin
import os

db_connect = os.environ['CONNECT_DB']
engine = create_engine(db_connect,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


class Base(DeclarativeBase):
  pass


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class User(Base, UserMixin):
  __tablename__ = 'users'
  user_id = mapped_column(Integer, primary_key=True)
  email = mapped_column(String(100), unique=True, nullable=False)
  first_name = mapped_column(String(40), nullable=False)
  last_name = mapped_column(String(40), nullable=False)
  phone = mapped_column(BigInteger, nullable=True)
  password = mapped_column(String(100), nullable=False)

  def get_id(self):
    return str(self.user_id)


class Contacts(Base):
  __tablename__ = 'contact_us'
  id = mapped_column(Integer, primary_key=True)
  fullname = mapped_column(String(100), nullable=False)
  email = mapped_column(String(150), nullable=False)
  contact_number = mapped_column(BigInteger, nullable=True)
  queries = mapped_column(String(300), nullable=False)
  status = mapped_column(SmallInteger, nullable=False)
  regdate = mapped_column(Date, nullable=False)


class Jobs(Base):
  __tablename__ = 'jobs'
  id = mapped_column(Integer, primary_key=True)
  title = mapped_column(String(250), nullable=False)
  location = mapped_column(String(250), nullable=False)
  salary = mapped_column(Integer, nullable=True)
  currency = mapped_column(String(10), nullable=True)
  responsibilities = mapped_column(String(2000), nullable=True)
  requirements = mapped_column(String(2000), nullable=True)
  status = mapped_column(SmallInteger, nullable=True)
  regdate = mapped_column(Date, nullable=True)
  enddate = mapped_column(Date, nullable=True)


class JobsApplied(Base):
  __tablename__ = 'jobs_applied'
  id = mapped_column(Integer, primary_key=True)
  job_id = mapped_column(Integer, nullable=False)
  title = mapped_column(String(150), nullable=False)
  email = mapped_column(String(150), nullable=False)
  linkedurl = mapped_column(String(150), nullable=False)
  work_experience = mapped_column(String(250), nullable=True)
  education = mapped_column(String(250), nullable=True)
  resumeurl = mapped_column(String(150), nullable=True)
  status = mapped_column(SmallInteger, nullable=False)
  regdate = mapped_column(Date, nullable=False)
  fullname = mapped_column(String(100), nullable=True)
