from sqlalchemy import *
from sqlalchemy.orm import *
import threading
from types import ModuleType
from helpers.schema import DB_PATH, _create_db
import time

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
    code += "    stmt += lambda s: s.where((A.col1 == wanted) & (A.col2 == wanted) & (A.col3 == wanted) & (A.col4 == wanted))\n"

code += """
    return stmt
"""

_create_db(THREADS)


class Runner(threading.Thread):
    def __init__(self, module, wanted) -> None:
        self.module = module
        self.wanted = wanted
        super().__init__()

    def run(self):
        self.module.generate_lambda_stmt(self.wanted)


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

stmt = module.generate_lambda_stmt(5)

e = create_engine(DB_PATH, echo=True)
with e.connect() as conn:
    row = conn.execute(stmt).first()

if not row:
    print(f"Failed on thread {5}")
else:
    print(f"Success on thread {5}")
