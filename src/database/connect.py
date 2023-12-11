from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

engine = create_engine(url=config.DATABASE_URL, echo=True)
Session = sessionmaker(engine)
