from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employer, Job
from app.settings.config import DB_URL
from app.db.data import employers_data, jobs_data

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        j = Job(**job)
        session.add(j)

    session.commit()
    session.close()
