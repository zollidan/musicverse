from sqlalchemy import create_engine

from models import Base


engine = create_engine("sqlite:///./test.db", echo=True)
Base.metadata.create_all(engine)