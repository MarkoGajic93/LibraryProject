from flask import render_template, flash, url_for
from werkzeug.utils import redirect

from app.author import author_bp
from app.author.forms import NewAuthorForm, DeleteAuthorForm
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

@author_bp.route("/new", methods=["GET", "POST"])
def add_new():
    conn = get_db()
    cursor = conn.cursor()
    form = NewAuthorForm()
    if form.validate_on_submit():
        cursor.execute("""INSERT INTO author (name, biography) VALUES (%s, %s)""",
                       (form.name.data, form.biography.data))
        conn.commit()
        flash(f"Author {form.name.data} added successfully.", "success")
        return redirect(url_for("author.view_all"))
    return render_template("new_author.html", form=form)

@author_bp.route("/delete", methods=["GET", "POST"])
def delete():
    conn = get_db()
    cursor = conn.cursor()
    form = DeleteAuthorForm()
    form.set_choices(cursor)
    if form.validate_on_submit():
        cursor.execute("""DELETE FROM author WHERE id=%s""", (form.name.data,))
        conn.commit()
        flash("Author deleted successfully.", "success")
        return redirect(url_for("author.view_all"))
    return render_template("delete_author.html", form=form)