from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend import config

DATABASE_URL = f"postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.DATABASE}"

# Create a synchronous engine
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

# Create a synchronous sessionmaker
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_models():
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)  # Drop all tables
        Base.metadata.create_all(conn)  # Create all tables

# Initialize models (call this when setting up the database)
init_models()
