from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.simple import PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Optional
from email_validator import validate_email, EmailNotValidError


def coerce_int(value):
    if isinstance(value, int):
        return value
    return int(value)


class RealEmail:
    """
    WTForms validator that checks the email is well-formed AND that its
    domain actually exists and can receive mail (MX/A record lookup).
    Rejects typos like 'gmial.com' or made-up domains, not just bad syntax.
    """
    def __init__(self, message=None):
        self.message = message or "Please enter a real, deliverable email address."

    def __call__(self, form, field):
        from wtforms.validators import ValidationError
        try:
            # check_deliverability=True triggers the DNS MX/A record lookup
            validate_email(field.data, check_deliverability=True)
        except EmailNotValidError:
            raise ValidationError(self.message)


#WTForm for adding a new task
class NewTask(FlaskForm):
    task = StringField("Task Item", validators=[DataRequired()])
    time = StringField("Time(e.g 8.30-9.00)", validators=[Optional()])
    grade = SelectField("What's the priority grade?",
                        validators=[DataRequired()], validate_choice=True,
                        choices=[(1, 'High'), (2, 'Moderate'), (3, 'Low')],
                        coerce=coerce_int)
    submit = SubmitField("Add task")

# Form for registering/sign-up as a new user
class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[
        DataRequired(),
        Email("Must be a valid email"),
        RealEmail()
    ])
    name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign me Up!")

# Form for logging in registered/existing users
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Invalid email.")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")
