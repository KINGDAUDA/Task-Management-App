import os
from datetime import date

from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect, CSRFError
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from functools import wraps
from typing import List

from unicodedata import category
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, NewTask


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "local-dev-key")
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash("Your session expired or the request looked suspicious — please try again.", category="error")
    return redirect(url_for("home"))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tasks.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# User table for all registered Users
class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    user_task: Mapped[List["Task"]] = relationship(back_populates="task_owner")


class Task(db.Model):
    __tablename__ = "Tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(250), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    task_owner: Mapped["User"] = relationship(back_populates="user_task")


with app.app_context():
    db.create_all()


# Register a new user
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    loginform = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        #Check if email already exists
        try:
            stmt = db.select(User).where(User.email == email)
            result = db.session.execute(stmt)
            existing_user = result.scalar_one()
            #If email exists, redirect to login
            flash("This email has already been registered."
                  " Please login instead.", category="error")
            return redirect(url_for("login"))
        except NoResultFound:
            # Email doesn't exist, proceed with registration
            salted_password = generate_password_hash(password, method="pbkdf2:sha256:600000", salt_length=8)
            new_user = User(
                email=form.email.data,
                password=salted_password,
                username=form.name.data
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("user_tasks"))
    return render_template("register.html", form=form)


# Login an existing user
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            stmt = db.select(User).where(User.email == email)
            result = db.session.execute(stmt)
            user = result.scalar_one()
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("user_tasks"))
            else:
                flash("Password incorrect")
                return redirect(url_for("login"))
        except NoResultFound:
            flash("Email does not exist")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
@login_required
def user_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all()
    return render_template("tasks.html", tasks=tasks)

@app.route("/new-task", methods=["GET", "POST"])
@login_required
def add_task():
    form = NewTask()
    if form.validate_on_submit():
        new_task = Task(
            task=form.task.data,
            grade=form.grade.data,
            task_owner=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("user_tasks"))
    return render_template("add_task.html", form=form)


@app.route("/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task_to_delete = db.get_or_404(Task, task_id)
    # To make sure people can only delete their own tasks.
    if task_to_delete.user_id != current_user.id:
        abort(403)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('user_tasks'))


# Called via fetch() when a task's checkbox is ticked. Deletes the task
# quietly in the background — the row itself stays visible (struck through)
# until the next page load/refresh, per the UX in tasks.html.
@app.route("/complete/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    task_to_complete = db.get_or_404(Task, task_id)
    if task_to_complete.user_id != current_user.id:
        abort(403)
    db.session.delete(task_to_complete)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(debug=False, port=5002)