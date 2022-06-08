from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import threading
from types import ModuleType

DB_PATH = "sqlite:///./any.db"

Base = declarative_base()


class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)
    col1 = Column(Text)
    col2 = Column(Text)
    col3 = Column(Text)
    col4 = Column(Text)


def _create_db():
    e = create_engine(DB_PATH, echo=True)
    Base.metadata.create_all(e)
    session = sessionmaker(e)()
    session.add_all(
        [
            A(col1="1", col2="1", col3="1", col4="1"),
            A(col1="2", col2="2", col3="2", col4="2"),
            A(col1="3", col2="3", col3="3", col4="3"),
            A(col1="4", col2="4", col3="4", col4="4"),
        ]
    )
    session.commit()
    session.close()
    e.dispose()
