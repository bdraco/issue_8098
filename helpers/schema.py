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
          [A(col1=str(i), col2=str(i), col3=str(i), col4=str(i)) for i in range(500)]
        ]
    )
    session.commit()
    session.close()
    e.dispose()
