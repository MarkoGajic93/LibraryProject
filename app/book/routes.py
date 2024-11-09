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
        cursor.execute("""SELECT id FROM book WHERE title=%s AND year_published=%s AND author_id=%s""",
                       (form.title.data.upper(), form.year_published.data, form.author.data))
        book_id = cursor.fetchone()

        if not book_id:
            cursor.execute("""INSERT INTO book (title, year_published, author_id) VALUES (%s,%s,%s) RETURNING id;""",
                           (form.title.data.upper(), form.year_published.data, form.author.data))
            book_id = cursor.fetchone()
            cursor.execute("""INSERT INTO warehouse_book (warehouse_id, book_id, quantity) VALUES (%s,%s,%s)""",
                           (form.warehouse.data, book_id, form.quantity.data))

        else:
            cursor.execute("""SELECT warehouse_id, quantity FROM warehouse_book WHERE book_id=%s""", (book_id,))
            warehouse_id, quantity = cursor.fetchone()

            if warehouse_id != form.warehouse.data:
                cursor.execute("""INSERT INTO warehouse_book (warehouse_id, book_id, quantity) VALUES (%s,%s,%s)""",
                               (form.warehouse.data, book_id, form.quantity.data))

            else:
                cursor.execute("""UPDATE warehouse_book SET quantity=%s WHERE warehouse_id=%s AND book_id=%s""",
                               (quantity+form.quantity.data, warehouse_id, book_id))

        conn.commit()
        flash(f"Book: {form.title.data.upper()} added successfully.", "success")
        return redirect(url_for("home.home"))

    return render_template("new_book.html", form=form)


def _setup_form(cursor) -> NewBookForm:
    form = NewBookForm()
    form.set_choices(cursor, "author")
    form.set_choices(cursor, "warehouse")
    return form
