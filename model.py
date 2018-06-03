"""Auditime model and database functions."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, time
from sqlalchemy import desc, asc, func

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


def duration_str(duration):
    """Format duration to a friendly string."""

    days = duration.days
    hours = duration.seconds / 3600
    minutes = (duration.seconds - hours * 3600) / 60

    duration_str = ""

    if duration.days > 0:
        duration_str += "{}d ".format(days)

    if hours > 0:
        duration_str += "{}h ".format(hours)

    if minutes > 0:
        duration_str += "{}m".format(minutes)

    return duration_str

##############################################################################
# Model definitions


class User(db.Model):
    """User."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id, self.email)


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

    def duration_str(self):
        return duration_str(self.duration)

    def total_time(self, time_period="all_time"):
        """Calculate total time spent on a goal."""

        goal_tasks = []
        for category in self.category:
            goal_tasks.extend(Task.query.filter_by(
                category_id=category.category_id))

        goal_events = []
        for task in goal_tasks:
            goal_events.extend(Event.query.filter_by(
                task_id=task.task_id).all())

        total_time = timedelta(0)
        today = datetime.today().date()

        # This past Sunday
        days_since_sun = (today.weekday() - 6) % 7
        sun = today - timedelta(days_since_sun)
        sun = datetime.combine(sun, time(0, 0))

        # This upcoming Saturday
        days_until_sat = (5 - today.weekday()) % 7
        sat = today + timedelta(days_until_sat)
        sat = datetime.combine(sat, time(23, 59))

        # This year and this month
        year = datetime.now().year
        month = datetime.now().month

        if time_period == 'this_week':
            start = sun
            end = sat
            print start, end

        elif time_period == 'last_week':
            start = sun - timedelta(7)
            end = sat - timedelta(7)

        elif time_period == 'this_month':
            start = datetime(year, month, 1, 0, 0)
            end = datetime(year, month + 1, 1, 23, 59) - timedelta(1)

        elif time_period == 'last_month':
            month = month - 1

            if month == 12:
                year = year - 1

            start = datetime(year, month, 1, 0, 0)
            end = datetime(year, month + 1, 1, 23, 59) - timedelta(1)

        elif time_period == 'all_time':
            start = datetime(1900, 1, 1, 0, 0)
            end = datetime.now()


        elif time_period == 'goal_time':
            start = self.start_time
            end = self.end_time

        for event in goal_events:

            # If the event starts and ends within the time period
            if event.start_time >= start and event.stop_time <= end:
                total_time += event.duration()

            # If the the event starts within the time period but ends after
            elif event.start_time <= end and event.start_time >= start:
                total_time += end - event.start_time

            # If the event ends within the time period but starts before
            elif event.stop_time >= start and event.stop_time <= end:
                total_time += event.stop_time - start

        return total_time


    def total_time_str(self, time_period='all_time'):

        return duration_str(self.total_time(time_period))

    def time_left(self):
        """Calculate the time left to reach goal target."""

        if self.duration >= self.total_time():
            time_left = self.duration - self.total_time()
            time_left_str = duration_str(time_left)

        else:
            time_left = self.total_time() - self.duration
            time_left_str = "-" + duration_str(time_left)

        return time_left_str

    def goal_status(self):
        """Return goal status."""

        # Success conditions
        if ((self.goal_type == "at_most" and self.total_time() <=
            self.duration and datetime.now() >= self.end_time) or
           (self.goal_type == "at_least" and self.total_time() >=
           self.duration)):
            time_left_str = "Success"

        # Fail conditions
        elif ((self.goal_type == "at_most" and self.total_time() >
              self.duration) or (self.goal_type == "at_least" and
              self.total_time() < self.duration and datetime.now() >=
              self.end_time)):
            time_left_str = "Fail"

        # Otherwise, show progress
        else:
            time_left_str = ""

        return time_left_str

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
    status = db.Column(db.String(64), nullable=True)

    # Define relationship to User, GoalCategory
    user = db.relationship("User", backref=db.backref("categories"))
    goal = db.relationship("Goal", secondary="goals_categories",
                           backref="categories")

    def duration(self, time_period='all_time'):

        total_time = timedelta(0)
        today = datetime.today().date()

        # This past Sunday
        days_since_sun = (today.weekday() - 6) % 7
        sun = today - timedelta(days_since_sun)
        sun = datetime.combine(sun, time(0, 0))

        # This upcoming Saturday
        days_until_sat = (5 - today.weekday()) % 7
        sat = today + timedelta(days_until_sat)
        sat = datetime.combine(sat, time(23, 59))

        # This year and this month
        year = datetime.now().year
        month = datetime.now().month

        if time_period == 'this_week':
            start = sun
            end = sat
            print start, end

        elif time_period == 'last_week':
            start = sun - timedelta(7)
            end = sat - timedelta(7)

        elif time_period == 'this_month':
            start = datetime(year, month, 1, 0, 0)
            end = datetime(year, month + 1, 1, 23, 59) - timedelta(1)

        elif time_period == 'last_month':
            month = month - 1

            if month == 12:
                year = year - 1

            start = datetime(year, month, 1, 0, 0)
            end = datetime(year, month + 1, 1, 23, 59) - timedelta(1)

        elif time_period == 'all_time':
            start = datetime(1900, 1, 1, 0, 0)
            end = datetime.now()

        for task in self.tasks:
            for event in task.events:

                # If the event starts and ends within the time period
                if event.start_time >= start and event.stop_time <= end:
                    total_time += event.duration()

                # If the the event starts within the time period but ends after
                elif event.start_time <= end and event.start_time >= start:
                    total_time += end - event.start_time

                # If the event ends within the time period but starts before
                elif event.stop_time >= start and event.stop_time <= end:
                    total_time += event.stop_time - start

        return total_time

    def duration_str(self, time_period='all_time'):
        """Returns the duration of the event as a formatted string."""

        return duration_str(self.duration(time_period))

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

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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


class Event(db.Model):
    """Stopwatch events."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    stop_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'),
                        nullable=False)
    status = db.Column(db.String(64), nullable=True)

    # Define relationship to Task, User
    task = db.relationship("Task", backref=db.backref("events"))
    user = db.relationship("User", backref=db.backref("events"))

    def duration(self):
        """Calculates and returns the duration of the event."""

        return self.stop_time - self.start_time

    def duration_str(self):
        """Returns the duration of the event as a formatted string."""

        return duration_str(self.duration())

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event event_id={} task_id={} user_id={}>".format(
            self.event_id, self.task_id, self.user_id)


class GoogleCalendar(db.Model):
    """Events imported from Google Calendar."""

    __tablename__ = "gcal_events"

    gcal_event_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'),
                         nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    stop_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    title = db.Column(db.Text, nullable=False)
    import_time = db.Column(db.DateTime, server_default=func.now(),
                            nullable=False)

    # Define relationship to Event, User
    event = db.relationship("Event", backref=db.backref("gcal_events"))
    user = db.relationship("User", backref=db.backref("gcal_events"))


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
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
