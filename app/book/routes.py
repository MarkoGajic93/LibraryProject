from flask import render_template, flash, url_for
from werkzeug.utils import redirect

from app.book import book_bp
from app.book.forms import NewBookForm
from db.db_service import get_db


@book_bp.route("/new", methods=["GET", "POST"])
def add_new():
    conn = get_db()
    cursor = conn.cursor()
    form = _setup_form(cursor)
    if form.validate_on_submit():
        cursor.execute("""INSERT INTO book (title, year_published, author_id) VALUES (%s,%s,%s) RETURNING id;""",
                       (form.title.data, form.year_published.data, form.author.data))
        print("book inserted into a table")
        book_uuid = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO warehouse_book (warehouse_id, book_id, quantity) VALUES (%s,%s,%s)""",
                       (form.warehouse.data, book_uuid, form.quantity.data))
        conn.commit()
        flash(f"Book: {form.title.data} added successfully.", "success")
        return redirect(url_for("home.home"))

    return render_template("new_book.html", form=form)


def _setup_form(cursor) -> NewBookForm:
    form = NewBookForm()
    form.set_choices(cursor, "author")
    form.set_choices(cursor, "warehouse")
    return form