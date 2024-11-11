from flask import render_template, flash, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app.auth import auth_bp
from app.auth.forms import MemberRegisterForm, MemberLoginForm
from db.db_service import get_db


@auth_bp.app_context_processor
def inject_current_user():
    return dict(current_user=get_current_user())

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

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    conn = get_db()
    cursor = conn.cursor()
    form = MemberLoginForm()
    if form.validate_on_submit():
        cursor.execute("""SELECT email, name, password FROM member WHERE email=%s""", (form.email.data,))
        email, name, hash_password = cursor.fetchone()
        if check_password_hash(hash_password, form.password.data):
            session["user"] = {'email': email, 'name': name}
            flash(f"{name} logged in successfully", "success")
            return redirect(url_for("home.home"))
        flash("Incorrect password", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    try:
        user = session.pop("user")
        flash(f"{user['name']} logged out.", "success")
    except KeyError:
        flash("You are not logged in.", "danger")
    return redirect(url_for("home.home"))

def get_current_user() -> dict:
    _current_user = getattr(g, "_current_user", None)
    if not _current_user:
        if session.get("user"):
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""SELECT email, name, age, phone_number FROM member WHERE email=%s""", (session['user']['email'],))
            email, name, age, phone = cursor.fetchone()
            _current_user = g._current_user = {"email": email, "name": name, "age": age, "phone": phone}
        else:
            _current_user = {}
    return _current_user
