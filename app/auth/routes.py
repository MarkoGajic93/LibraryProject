from flask import render_template, flash, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from app.auth import auth_bp
from app.auth.forms import MemberRegisterForm
from db.db_service import get_db


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = MemberRegisterForm()
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(form.password.data)
        cursor.execute("INSERT INTO member (email, name, password, age, phone_number) VALUES (%s,%s,%s,%s,%s)",
                       (form.email.data, form.name.data, hashed_password, form.age.data, form.phone.data))
        conn.commit()
        flash(f"{form.name.data} successfully registered.", "success")
        return redirect(url_for('home.home'))
    return render_template("register.html", form=form)