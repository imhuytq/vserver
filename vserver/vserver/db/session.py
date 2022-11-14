from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vserver.config import config


engine = create_engine(config.DATABASE_DSN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
