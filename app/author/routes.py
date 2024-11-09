from flask import render_template

from app.author import author_bp
from db.db_service import get_db


@author_bp.route("/")
def view_all():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""SELECT id, name, biography FROM author""")
    authors_in_db = cursor.fetchall()
    authors = []
    for row in authors_in_db:
        author = {
            "id": row[0],
            "name": row[1],
            "biography": row[2]
        }
        authors.append(author)
    return render_template("authors.html", authors=authors)