from sqlalchemy import *
from sqlalchemy.orm import *
import threading
from types import ModuleType
from helpers.schema import DB_PATH, _create_db
import time

from sqlalchemy.sql import lambdas
from sqlalchemy import util

lambdas._closure_per_cache_key = util.LRUCache(1)

THREADS = 4
NUM_OF_LAMBDAS = 180  # Increase this number if your system is fast


code = """
from helpers.schema import A
from sqlalchemy import *
from sqlalchemy.orm import *


def generate_lambda_stmt(wanted):
    stmt = lambda_stmt(lambda: select(A.col1, A.col2, A.col3, A.col4))

"""

for _ in range(NUM_OF_LAMBDAS):
    code += "    stmt += lambda s: s.where((A.col1 == wanted))\n"
    code += "    stmt += lambda s: s.where((A.col2 == wanted))\n"
    code += "    stmt += lambda s: s.where((A.col3 == wanted))\n"
    code += "    stmt += lambda s: s.where((A.col4 == wanted))\n"

code += """
    return stmt
"""

_create_db()


class Runner(threading.Thread):
    def __init__(self, module, wanted) -> None:
        self.module = module
        self.wanted = wanted
        super().__init__()

    def run(self):
        e = create_engine(DB_PATH, echo=True)
        session = sessionmaker(e)()
        stmt = self.module.generate_lambda_stmt(self.wanted)
        row = session.execute(stmt).first()
        if not row or [val for val in row if val != self.wanted]:
            print(f"Failed on thread {self.wanted}")
            time.sleep(1000)
        else:
            print(f"Success on thread {self.wanted}")
        session.close()
        e.dispose()


compiled = compile(code, "onetime.py", "exec")
module = ModuleType("lambda_fake")
exec(compiled, module.__dict__)
threads = []
for num in range(THREADS):
    threads.append(Runner(module, str(num + 1)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
