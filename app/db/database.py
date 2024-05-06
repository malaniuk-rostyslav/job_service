from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.settings.config import DB_URL


engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def prepare_database():
    Base.metadata.create_all(engine)