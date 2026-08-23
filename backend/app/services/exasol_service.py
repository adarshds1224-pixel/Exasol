import os

import pyexasol
from dotenv import load_dotenv

load_dotenv()


def get_exasol_connection():
    return pyexasol.connect(
        dsn=os.environ["EXASOL_DSN"],
        user=os.environ["EXASOL_USER"],
        password=os.environ["EXASOL_PASSWORD"],
        encryption=True,
        websocket_sslopt={"cert_reqs": 0},
        fetch_dict=True,
    )