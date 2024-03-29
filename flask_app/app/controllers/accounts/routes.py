from dependency_injector.wiring import inject, Provide

from app import bcrypt, db
from app.controllers.accounts import bp
from app.models.UserModel import User
from app.services.decorators import logout_required
from app.services.emails.email_sender import EmailSender
from app.services.forms import ConfirmEmailForm, LoginForm, RegisterForm
from app.services.token import TokenService
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.containers import Container


@bp.route("/register", methods=["GET", "POST"])
@logout_required
@inject
def register(email_service: EmailSender = Provide[Container.email_service]):
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = TokenService.generate_token(email=form.email.data)

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")
        try:
            email_service.send_email(
                message=f"Token: {token}", subject="Your token", recipient=user.email
            )
            flash(f"Token has been sent on {user.email}", "success")
        except Exception:
            flash("Couldn't generate email token")
        flash(f"token: {token}")
        return redirect(url_for("main.home"))

    return render_template("accounts/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        """Check if user is in DB"""
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You have logged in successfully", "success")
            return redirect(url_for("main.home"))
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


@bp.route("/confirm", methods=["GET", "POST"])
@login_required
def confirm_account():
    if current_user.is_confirmed:
        flash("Account is already confirmed.", "success")
        return redirect(url_for("main.home"))

    form = ConfirmEmailForm(request.form)
    if form.validate_on_submit():
        uploaded_token = form.token.data
        email = TokenService.confirm_token(uploaded_token)
        user = User.query.filter_by(email=current_user.email).first_or_404()

        if user.email == email:
            user.is_confirmed = True
            db.session.add(user)
            db.session.commit()
            flash("You have confirmed your account. Thanks!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("The confirmation link is invalid or has expired.", "danger")

    return render_template("accounts/confirm_account.html", form=form)


@bp.route("/resend", methods=["GET", "POST"])
@login_required
@inject
def resend_token(email_service: EmailSender = Provide[Container.email_service]):
    """Get current user email crom current_user.email global variable attached to user session,
    and send token again"""  # noqa: E501
    if current_user.email:
        token = TokenService.generate_token(email=current_user.email)
        try:
            email_service.send_email(
                message=f"Token: {token}",
                subject="Your token",
                recipient=current_user.email,
            )
            flash(f"Token has been sent on {current_user.email}", "success")
        except Exception:
            flash("Couldn't generate email token")
        flash(f"token: {token}")
        return redirect(url_for("accounts.confirm_account"))

    return redirect(url_for("accounts.confirm_account"))
