
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import bcrypt, db
from app.models.models import User
from app.services.forms import LoginForm, RegisterForm
from app.services.token import generate_token, confirm_token
from app.services.decorators import check_is_confirmed, logout_required
from app.controllers.accounts import bp




@bp.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = generate_token(email=form.email.data)

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")
        flash(f"Token: {token}")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
@logout_required
def login():

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash("You have logged in successfully", "success")

            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))


@bp.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("core.home"))

    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()

    if user.email == email:
        user.is_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("core.home"))


