from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.simple import PasswordField, EmailField
from wtforms.validators import DataRequired, Email


def coerce_int(value):
    if isinstance(value, int):
        return value
    return value in (1, 2, 3)

#WTForm for adding a new task
class NewTask(FlaskForm):
    task = StringField("Task Item", validators=[DataRequired()])
    grade = SelectField("What's the priority grade?",
                        validators=[DataRequired()], validate_choice=True,
                        choices=[(1, 'High'), (2, 'Moderate'), (3, 'Low')],
                        coerce=coerce_int)
    submit = SubmitField("Add task")

# Form for registering/sign-up as a new user
class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Must be a valid email")])
    name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign me Up!")

# Form for logging in registered/existing users
class LoginForm(FlaskForm):
    email = EmailField("Username", validators=[DataRequired(), Email("Invalid email.")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")