from flask import render_template

from db.db_service import get_db
from . import home_bp


@home_bp.route("/")
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""SELECT b.id, b.title, b.year_published, a.name, w.name, wb.quantity FROM book AS b
                      INNER JOIN author AS a ON b.author_id=a.id
                      INNER JOIN warehouse_book AS wb ON wb.book_id=b.id
                      INNER JOIN warehouse AS w ON w.id=wb.warehouse_id""")
    books_from_db = cursor.fetchall()
    books = []
    book_dict = {}
    if books_from_db:
        for row in books_from_db:
            book_id = row[0]
            title = row[1]
            year_published = row[2]
            author = row[3]
            warehouse = row[4]
            quantity = row[5]

            if book_id not in book_dict:
                book_dict[book_id] = {
                    'id': book_id,
                    'title': title,
                    'year_published': year_published,
                    'author': author,
                    'warehouses': {}
                }

            book_dict[book_id]['warehouses'][warehouse] = quantity

        books = list(book_dict.values())

    return render_template("home.html", books=books)