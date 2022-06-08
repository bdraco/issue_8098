from sqlalchemy import *
from sqlalchemy.orm import *
import threading
from types import ModuleType
from sqlalchemy.sql.elements import BindParameter
from sqlalchemy.sql.traversals import CacheKey
from helpers.schema import DB_PATH, _create_db
import time
import re


THREADS = 16
NUM_OF_LAMBDAS = 90  # Increase this number if your system is fast


from helpers.schema import A
from sqlalchemy import *
from sqlalchemy.orm import *


def generate_stmt(wanted):
    stmt = select(A.col1, A.col2, A.col3, A.col4)
    stmt = stmt.where(
        (A.col1 == wanted)
        & (A.col2 == wanted)
        & (A.col3 == wanted)
        & (A.col4 == wanted)
    )
    return stmt


_create_db()


class Runner(threading.Thread):
    def __init__(self, wanted) -> None:
        self.wanted = wanted
        super().__init__()

    def run(self):
        e = create_engine(DB_PATH, echo=True, logging_name=f"Thread {self.wanted}")
        session = sessionmaker(e)()
        stmt = generate_stmt(self.wanted)
        row = session.execute(stmt).first()
        if not row:
            print(f"Failed on thread {self.wanted}: {row}")
            time.sleep(1000)
        else:
            print(f"Success on thread {self.wanted} {row}")
        session.close()
        e.dispose()


threads = []
for num in range(THREADS):
    threads.append(Runner(str(num + 1)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
