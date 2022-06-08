from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import threading
from types import ModuleType
from sqlalchemy import create_engine, event as sqlalchemy_event

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

    def setup_recorder_connection(dbapi_connection, connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.close()

    sqlalchemy_event.listen(e, "connect", setup_recorder_connection)
    Base.metadata.create_all(e)
    session = sessionmaker(e)()
    session.add_all(
        [[A(col1=str(i), col2=str(i), col3=str(i), col4=str(i)) for i in range(500)]]
    )
    session.commit()
    session.close()
    e.dispose()
