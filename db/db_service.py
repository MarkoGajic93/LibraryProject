import psycopg2
from flask import g, current_app


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(current_app.config["DATABASE"])
    return g.db

def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()