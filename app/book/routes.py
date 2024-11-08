from app.book import book_bp


@book_bp("/new", methods=["GET", "POST"])
def add_new_book():
    pass