from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """Check if user is currently logged in.
        If yes, return flash object with info, else continue"""
        if current_user.is_authenticated:
            flash("You are already logged in.", "info")
            return redirect(url_for("main.home"))

        return func(*args, **kwargs)

    return decorated_function


def confirmed_user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """Check if user is confirmed by token"""
        if current_user.is_confirmed is False:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("main.home"))
        return func(*args, **kwargs)

    return decorated_function


def admin_user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """Check if user is admin"""
        if current_user.is_admin is False:
            flash("You are not admin!", "warning")
            return redirect(url_for("main.home"))
        return func(*args, **kwargs)

    return decorated_function
