"""Auditime model and database functions."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import desc, asc

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id,
                                                   self.email)


class Goal(db.Model):
    """Task."""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    goal_type = db.Column(db.String(64), nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)

    # Define relationship to User, GoalCategory
    user = db.relationship("User", backref=db.backref("goals"))
    category = db.relationship("Category", secondary="goals_categories",
                               backref="goals")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Goal goal_id={} name={} user_id={}>".format(
            self.goal_id, self.name, self.user_id)


class Category(db.Model):
    """Category."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True,
                            primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)

    # Define relationship to User, GoalCategory
    user = db.relationship("User", backref=db.backref("categories"))
    goal = db.relationship("Goal", secondary="goals_categories",
                           backref="categories")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id={} name={}>".format(
            self.category_id,
            self.name)


class GoalCategory(db.Model):
    """Association table for Goal and Category."""

    __tablename__ = 'goals_categories'

    goal_category_id = db.Column(db.Integer,
                                 autoincrement=True,
                                 primary_key=True)
    goal_id = db.Column(db.Integer,
                        db.ForeignKey('goals.goal_id'),
                        nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'),
                            nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<GoalCategory goal_id={} category_id={}>".format(
            self.goal_id,
            self.category_id)


class Task(db.Model):
    """Task."""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'),
                            nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)

    # Define relationship to Category, User.
    category = db.relationship("Category", backref=db.backref("tasks"))
    user = db.relationship("User", backref=db.backref("tasks"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Task task_id={} name={} user_id={}>".format(
            self.task_id, self.name, self.user_id)


class TaskCategory(db.Model):
    """Association table for Task and Category."""

    __tablename__ = 'tasks_categories'

    task_category_id = db.Column(db.Integer,
                                 autoincrement=True,
                                 primary_key=True)
    task_id = db.Column(db.Integer,
                        db.ForeignKey('tasks.task_id'),
                        nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'),
                            nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<TaskCategory task_id={} category_id={}>".format(
            self.task_id,
            self.category_id)


class Event(db.Model):
    """Stopwatch events."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True,
                         primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    stop_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'),
                        nullable=False)

    # Define relationship to Task, Category, User
    task = db.relationship("Task", backref=db.backref("events"))
    user = db.relationship("User", backref=db.backref("events"))

    def duration(self):
        """Calculates and returns the duration of the event."""

        return self.stop_time - self.start_time

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event event_id={} task_id={} user_id={}>".format(
            self.event_id, self.task_id, self.user_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///audittime'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    # Create tables if they don't already exist.
    db.create_all()
