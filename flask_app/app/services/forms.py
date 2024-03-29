from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
    BooleanField,
    SelectField,
    IntegerField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.UserModel import User


class SubscriptionUpdate(FlaskForm):
    notification_frequency = IntegerField()
    notify_on_price_change = SelectField("Test", choices=[("Yes"), ("No")])


class SubscribeProductForm(FlaskForm):
    subscribe_button = SubmitField()
    unsubscribe_button = SubmitField()


class ConfirmEmailForm(FlaskForm):
    token = StringField("token", validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """Do zrobienia te walidatory!"""

    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
