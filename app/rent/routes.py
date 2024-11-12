import uuid

from flask import flash, redirect, url_for, current_app, g, render_template, session

from app.auth.routes import get_current_user
from app.rent import rent_bp
from db.db_service import get_db


@rent_bp.route("/<uuid:book_id>", methods=["GET", "POST"])
def rent(book_id: uuid.UUID):
    if not get_current_user().get('email'):
        flash("You need to be logged in.", "danger")
        return redirect(url_for("home.home"))

    conn = get_db()
    cursor = conn.cursor()
    user_email = get_current_user().get('email')
    if user_email != current_app.config["ADMIN_EMAIL"]:
        cursor.execute("""SELECT b.id, b.title, wb.warehouse_id, wb.quantity FROM book AS b
                          INNER JOIN warehouse_book AS wb ON b.id=wb.book_id
                          WHERE b.id=%s""", (str(book_id),))
        id_of_book, title, warehouse_id, quantity = cursor.fetchone()
        print(id_of_book, title, warehouse_id, quantity)
        if quantity:
            session.setdefault('member_basket', {})
            user_basket = session['member_basket'].setdefault(user_email, {})

            if str(book_id) in user_basket:
                flash("This book is already in your basket.", "danger")
            else:
                user_basket[str(book_id)] = [title, warehouse_id]
                cursor.execute("""UPDATE warehouse_book SET quantity=%s 
                                  WHERE warehouse_id=%s AND book_id=%s""", ((quantity-1), warehouse_id, id_of_book))
                conn.commit()
                flash("Book added to your rent basket.", "success")
        else:
            flash("Sorry, all copies of this book are currently rented", "danger")
    return redirect(url_for("home.home"))

@rent_bp.route("/basket")
def view_basket():
    if not get_current_user().get('email'):
        flash("You need to be logged in.", "danger")
        return redirect(url_for("home.home"))

    books_in_basket = get_basket()
    return render_template("basket.html", books=list(books_in_basket.values()))

def get_basket() -> dict:
    basket = session.get("member_basket")
    books_in_basket = {}
    if basket:
        books_in_basket = basket[get_current_user().get("email")]
    return books_in_basket

