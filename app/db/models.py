from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey


Base = declarative_base()


class Employer(Base):
    __tablename__ = 'employers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_email = Column(String)
    industry = Column(String)


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey('employers.id'))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    role = Column(String)


class JobApplication(Base):
    __tablename__ = 'job_applications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
