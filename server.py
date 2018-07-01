"""Auditime server."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Category, Event, Task, Goal, \
                  GoalCategory, GoogleCalendar, TogglEntry
from datetime import datetime, timedelta
from dateutil.parser import parse
from addNew import goal_generate_html, category_generate_html, task_generate_html
from math import floor
from gcal import gcal_get_last_7_days, gcal_update_db
from toggl import toggl_get_last_7_days, toggl_update_db
import json
import pdb
import hashlib


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


# ------------------------------ AUTHENTICATION ------------------------------
@app.route('/')
def display_index():
    """Display homepage."""

    try:
        if session['user']:
            return redirect('/tasks')

    except:
        return redirect('/login')


@app.route('/signup')
def display_signup():
    """Display signup form."""

    return render_template('signup.html')


@app.route('/signup_submit', methods=['POST'])
def submit_signup():
    """Collect login information and log user in."""

    name = request.form.get('name')
    email = request.form.get('email')
    password = hashlib.sha256(request.form.get('password')).hexdigest()

    new_user = User(name=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    session['user'] = email
    session['user_id'] = new_user.user_id

    return 'success'


@app.route('/login')
def display_login():
    """Display login form."""

    return render_template('login.html')


@app.route('/login_submit', methods=['POST'])
def submit_login():
    """Collect login information and log user in."""

    email = request.form.get('email')
    password = hashlib.sha256(request.form.get('password')).hexdigest()

    try:
        if User.query.filter_by(email=email).one().password == password:
            session['user'] = email
            session['user_id'] = User.query.filter_by(
                email=email).one().user_id

        return "success"

    except:
        return "fail"


@app.route('/logout')
def logout():
    """Log user out of session."""

    session.pop('user')
    session.pop('user_id')

    return redirect('/')


# ----------------------------------- GOALS -----------------------------------

@app.route('/goals')
def display_goals():
    """Display goals page."""

    goals = db.session.query(Goal).filter_by(
        user_id=session['user_id'], status='active').order_by(
        'end_time').all()

    categories = db.session.query(Category).filter_by(
        user_id=session['user_id'], status='current').order_by('name').all()

    return render_template("goals.html", goals=goals, categories=categories)


@app.route('/add_goal', methods=['POST'])
def add_goal():
    """Adds a goal to the goals table."""

    goal_name = str(request.form.get('goalName'))
    goal_type = request.form.get('goalType')
    hours = int(request.form.get('hours'))
    minutes = int(request.form.get('minutes'))
    duration = timedelta(hours=hours, minutes=minutes)
    start_time = request.form.get('startDate')
    end_time = request.form.get('endDate')
    user_id = session['user_id']

    # Convert start and end times to correct format
    start_time = parse(start_time)
    end_time = parse(end_time)

    new_goal = Goal(name=goal_name, start_time=start_time, end_time=end_time,
                    goal_type=goal_type, duration=duration, status="active",
                    user_id=user_id)

    db.session.add(new_goal)
    db.session.commit()

    goal = Goal.query.filter_by(name=goal_name, end_time=end_time,
                                user_id=user_id).one()

    goal_id = str(goal.goal_id)
    goal_category = goal.category
    total_time = goal.total_time_str("goal_time")
    time_left = goal.time_left()
    goal_status = goal.goal_status()

    categories = Category.query.filter_by(user_id=user_id).all()

    new_goal_html = goal_generate_html(total_time, goal_id, goal_name,
                                       goal_type,
                                       duration.days, str(hours), str(minutes),
                                       start_time, end_time, time_left,
                                       goal_status, categories,
                                       goal_category)

    return new_goal_html


@app.route('/edit_goal_info', methods=['POST'])
def edit_goal_info():
    """Updates new goal info in the goals table."""

    user_id = session['user_id']
    goal_id = request.form.get('goalId')
    new_goal_name = request.form.get('newGoalName')
    new_days = int(request.form.get('newDays'))
    new_hours = int(request.form.get('newHours'))
    new_minutes = int(request.form.get('newMinutes'))
    new_duration = timedelta(days=new_days, hours=new_hours,
                             minutes=new_minutes)
    new_type = request.form.get('newType')
    goal = Goal.query.filter_by(goal_id=goal_id).one()

    # Update name and duration
    goal.name = new_goal_name
    goal.duration = new_duration
    goal.type = new_type

    if request.form.get('newStartTime'):
        new_start = request.form.get('newStartTime')
        new_start = datetime.strptime(new_start, "%m/%d at %I:%M %p")
        goal.start_time = new_start

    if request.form.get('newEndTime'):
        new_end = request.form.get('newEndTime')
        new_end = datetime.strptime(new_end, "%m/%d at %I:%M %p")
        goal.end_time = new_end

    new_category_goals = request.form.get('newCategoryGoals')
    new_category_goals = new_category_goals.split('|')[:-1]

    # Clear the goal's current categories and add the new ones
    goal.categories = []

    for category in new_category_goals:
        new_category = Category.query.filter_by(user_id=user_id, name=category).one()
        new_goal_category = GoalCategory(goal_id=goal_id,
                                         category_id=new_category.category_id)
        db.session.add(new_goal_category)

    db.session.commit()

    return redirect('/goals')


@app.route('/archive_goal', methods=['POST'])
def archive_goal():
    """Archive a goal."""

    # Grab data from form via JavaScript
    goal_id = request.form.get('goalId')

    # Find the existing goal
    goal = Goal.query.filter_by(goal_id=goal_id).one()

    # Set status to 'archived'
    goal.status = 'archived'
    db.session.commit()

    return "goal archived"


# -------------------------------- CATEGORIES --------------------------------

@app.route('/categories')
def display_categories():
    """Display goals page."""

    goals = db.session.query(Goal).filter_by(
        user_id=session['user_id']).order_by(
        'end_time').all()

    categories = db.session.query(Category).filter_by(
        user_id=session['user_id'],
        status='current').order_by('name').all()

    return render_template("categories.html", goals=goals,
                           categories=categories)


@app.route('/add_category', methods=['POST'])
def add_category():
    """Adds a category to the categories table."""

    # Grab data from form via JavaScript
    category_name = request.form.get('categoryName')
    category_goals = request.form.get('categoryGoals')
    category_goals = category_goals.split('|')[:-1]
    user_id = session['user_id']

    print category_goals, "HELLOOOOOOOOOOOOOOOO"

    # Add new category to the categories table.
    new_category = Category(name=category_name, user_id=user_id,
                            status='current')
    db.session.add(new_category)
    db.session.commit()

    # Add new goal associations to the goals_categories table.
    category_id = new_category.category_id

    for goal_name in category_goals:
        goal_id = Goal.query.filter_by(name=goal_name, user_id=user_id).one(
            ).goal_id

        new_goal_category = GoalCategory(goal_id=goal_id,
                                         category_id=category_id)
        db.session.add(new_goal_category)

    db.session.commit()

    all_goals = Goal.query.all()

    category_html = category_generate_html(category_id, category_name,
                                           all_goals, category_goals)

    return category_html


@app.route('/edit_category_info', methods=['POST'])
def edit_category_info():
    """Updates new category info in the categories table."""

    # Grab data from form via JavaScript
    category_id = request.form.get('categoryId')
    new_category_name = request.form.get('newcategoryName')

    new_category_goals = request.form.get('newCategoryGoals')
    new_category_goals = new_category_goals.split('|')[:-1]
    user_id = session['user_id']

    # Find the existing category
    category = Category.query.filter_by(category_id=category_id).one()

    # Update name and goals
    category.name = new_category_name
    category.goal = []

    for goal_name in new_category_goals:
        goal_id = Goal.query.filter_by(name=goal_name, user_id=user_id).one(
            ).goal_id

        new_goal_category = GoalCategory(goal_id=goal_id,
                                         category_id=category_id)
        db.session.add(new_goal_category)

    db.session.commit()

    return "category updated"


@app.route('/archive_category', methods=['POST'])
def archive_category():
    """Archive a category."""

    # Grab data from form via JavaScript
    category_id = request.form.get('categoryId')

    # Find the existing category
    category = Category.query.filter_by(category_id=category_id).one()

    # Set status to 'archived'
    category.status = 'archived'
    db.session.commit()

    return "category archived"


# ---------------------------------- TASKS ---------------------------------

@app.route('/tasks')
def display_tasks():
    """Display tasks page."""

    categories = db.session.query(Category).filter_by(
        user_id=session['user_id']).order_by('name').all()

    events = db.session.query(Event).filter_by(
        user_id=session['user_id'], status='active').order_by('stop_time').all()

    # Display log in reverse chronological order.
    events.reverse()

    return render_template("tasks.html", events=events,
                           categories=categories)


@app.route('/add_event', methods=['POST'])
def add_event():
    """Adds a new event to the database."""

    form_data = request.form
    start_time = form_data['startTime']
    stop_time = form_data['stopTime']

    # If the event was added via stopwatch (i.e., data returned as a string),
    # do some additional processing for the start/stop times. (The length of
    # the timestamp returned by manual submission is 16, whereas UTC is ~13.)
    if len(stop_time) < 16:

        # Convert from JavaScript (milliseconds) to Python (seconds).
        start_time = int(start_time)/1000
        stop_time = int(stop_time)/1000

        # Convert from seconds to proper timestamp.
        start_time = datetime.utcfromtimestamp(start_time)
        stop_time = datetime.utcfromtimestamp(stop_time)

    task_name = form_data['task']
    category_name = form_data['category']
    status = 'active'
    user_id = User.query.filter_by(email=session['user']).one().user_id

    # If the task already exists, find its id.
    if Task.query.filter_by(name=task_name).first():
        task_id = Task.query.filter_by(name=task_name).first().task_id

    else:
        # Create a new task.
        # If the category already exists, find its id.
        try:
            if int(Category.query.filter_by(name=category_name).first(
                   ).user_id) == int(user_id):
                category_id = Category.query.filter_by(name=category_name) \
                    .first().category_id

        except():
            # Create a new category.
            new_category = Category(name=category_name,
                                    user_id=user_id)

            db.session.add(new_category)
            db.session.commit()

            # Find the newly created category's id.
            category_id = Category.query.filter_by(name=category_name) \
                .first().category_id

            category_id = new_category.category_id

        # With the category_id, we now have enough info to create the new task.
        new_task = Task(name=task_name, category_id=category_id,
                        user_id=user_id)

        db.session.add(new_task)
        db.session.commit()

        # Find the newly created task's id.
        task_id = Task.query.filter_by(name=task_name).first().task_id
        task_id = new_task.task_id

    # With the task_id, we now have enough info to create the new event.
    new_event = Event(start_time=start_time, stop_time=stop_time,
                      user_id=user_id, task_id=task_id, status=status)

    db.session.add(new_event)
    db.session.commit()

    event = Event.query.filter_by(task_id=task_id, stop_time=stop_time).one()

    categories = Category.query.filter_by(user_id=user_id).all()
    start = event.start_time.strftime('%m/%d at %I:%M %p')
    stop = event.stop_time.strftime('%m/%d at %I:%M %p')
    duration = event.duration_str()

    form_html = task_generate_html(event_id=event.event_id,
                                   task_id=event.task.task_id,
                                   task_name=event.task.name,
                                   category_name=event.task.category.name,
                                   all_categories=categories,
                                   start=start, stop=stop,
                                   duration=duration)

    return form_html


@app.route('/edit_task', methods=['POST'])
def edit_task():
    """Updates task"""

    event_id = request.form.get('eventId')
    new_task_name = request.form.get('newTaskName')
    new_start_time = request.form.get('newStartTime')
    new_stop_time = request.form.get('newStopTime')

    category_id = Event.query.filter_by(event_id=event_id).one(
        ).task.category_id
    user_id = session['user_id']

    # If the new task already exists, find its id.
    if Task.query.filter_by(name=new_task_name).first():
        new_task_id = Task.query.filter_by(name=new_task_name).first().task_id

    else:
        # Create a new task.
        new_task = Task(name=new_task_name, category_id=category_id,
                        user_id=user_id)

        db.session.add(new_task)
        db.session.commit()

        new_task_id = Task.query.filter_by(name=new_task_name).one().task_id

    # Reassign event's task id to the new task id.
    event = Event.query.filter_by(event_id=event_id).one()
    event.task_id = new_task_id

    # If the start/stop times were edited, save them.
    if new_start_time:
        new_start_time = datetime.strptime(new_start_time, "%m/%d at %I:%M %p")
        event.start_time = new_start_time

    if new_stop_time:
        new_start_time = datetime.strptime(new_stop_time, "%m/%d at %I:%M %p")
        event.stop_time = new_stop_time

    db.session.commit()

    return redirect('/tasks')


@app.route('/archive_event', methods=['POST'])
def archive_event():
    """Archive an event."""

    # Grab data from form via JavaScript
    event_id = request.form.get('eventId')

    # Find the existing event
    event = Event.query.filter_by(event_id=event_id).one()

    # Set status to 'archived'
    event.status = 'archived'
    db.session.commit()

    return "event archived"


@app.route('/toggl')
def load_toggl():
    """Displays entries from Toggl."""

    user_id = session['user_id']
    api_token = User.query.filter_by(user_id=user_id).one().toggl_token

    # Grab last 7 days of Toggle entries and update the database.
    toggl_update_db(user_id, api_token)

    categories = db.session.query(Category).filter_by(
        user_id=session['user_id']).order_by('name').all()

    goals = db.session.query(Goal).filter_by(
        user_id=session['user_id']).order_by(
        'end_time').all()

    toggl_entries = TogglEntry.query.filter_by(status='pending').all()

    return render_template("toggl.html", toggl_entries=toggl_entries,
                           categories=categories, goals=goals)


@app.route('/delete_toggl_entry', methods=['POST'])
def delete_toggl_entry():
    """When user imports Google Calendar events and deletes ones, update
    toggl_entries table status as 'deleted'."""

    toggl_entry_id = request.form.get('togglEntryId')

    toggl_entry = TogglEntry.query.filter_by(toggl_entry_id=toggl_entry_id).one()
    toggl_entry.status = 'deleted'

    db.session.commit()

    return redirect('/toggl')


@app.route('/save_toggl_entry', methods=['POST'])
def save_toggl_entry():
    """When user imports Google Calendar events and saves ones, update
    toggl_entries table status as 'saved', create a new task and new event."""

    toggl_entry_id = request.form.get('togglEntryId')
    category_name = request.form.get('categoryName')
    user_id = session['user_id']
    print category_name
    category_id = Category.query.filter_by(name=category_name,
                                           user_id=user_id).one().category_id

    # Update status in toggl_entries table to 'saved'
    toggl_entry = TogglEntry.query.filter_by(
        toggl_entry_id=toggl_entry_id).one()

    toggl_entry.status = 'saved'

    # Create new task and add to database
    new_task = Task(name=toggl_entry.title,
                    category_id=category_id,
                    user_id=user_id)

    db.session.add(new_task)
    db.session.commit()

    # Create new event and add to database
    task_id = new_task.task_id

    new_event = Event(start_time=toggl_entry.start_time,
                      stop_time=toggl_entry.stop_time,
                      user_id=user_id,
                      task_id=task_id,
                      status='active')

    db.session.add(new_event)

    # Update toggl_entries table with new event_id
    toggl_entry.event_id = new_event.event_id

    db.session.commit()

    return redirect('/toggl')


@app.route('/settings')
def display_settings():
    """Displays account settings for a user."""

    return render_template("settings.html")


@app.route('/save_settings', methods=['POST'])
def save_settings():
    """Update database with new settings information."""

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    toggl_token = request.form.get('toggl-token')

    user = User.query.filter_by(user_id=session['user_id']).one()

    if name:
        user.name = name

    if email:
        user.email = email

    if password:
        user.password = hashlib.sha256(password).hexdigest()

    if toggl_token:
        user.toggl_token = toggl_token

    db.session.commit()

    return redirect('/settings')


@app.route('/gcal')
def display_gcal_events():
    """Shows pending Google Calendar events that aren't yet saved as 
    tasks."""

    # Grab last 7 days of Google Calendar events and update the database.
    gcal_update_db(session['user_id'])

    categories = db.session.query(Category).filter_by(
        user_id=session['user_id']).order_by('name').all()

    goals = db.session.query(Goal).filter_by(
        user_id=session['user_id']).order_by(
        'end_time').all()

    gcal_events = GoogleCalendar.query.filter_by(status='pending').all()

    return render_template("gcal.html", gcal_events=gcal_events,
                           categories=categories, goals=goals)


@app.route('/delete_gcal_event', methods=['POST'])
def delete_gcal_event():
    """When user imports Google Calendar events and deletes ones, update
    gcal_events table status as 'deleted'."""

    gcal_event_id = request.form.get('gcalEventId')

    event = GoogleCalendar.query.filter_by(gcal_event_id=gcal_event_id).one()
    event.status = 'deleted'

    db.session.commit()

    return redirect('/gcal')


@app.route('/save_gcal_event', methods=['POST'])
def save_gcal_event():
    """When user imports Google Calendar events and saves ones, update
    gcal_events table status as 'saved', create a new task and new event."""

    gcal_event_id = request.form.get('gcalEventId')
    category_name = request.form.get('categoryName')

    print category_name
    user_id = session['user_id']
    category_id = Category.query.filter_by(name=category_name,
                                           user_id=user_id).one().category_id


    # Update status in gcal_events table to 'saved'
    gcal_event = GoogleCalendar.query.filter_by(
        gcal_event_id=gcal_event_id).one()

    gcal_event.status = 'saved'

    # Create new task and add to database
    new_task = Task(name=gcal_event.title,
                    category_id=category_id,
                    user_id=user_id)

    db.session.add(new_task)
    db.session.commit()

    # Create new event and add to database
    task_id = new_task.task_id

    new_event = Event(start_time=gcal_event.start_time,
                      stop_time=gcal_event.stop_time,
                      user_id=user_id,
                      task_id=task_id,
                      status='active')

    db.session.add(new_event)

    # Update gcal_events table with new event_id
    gcal_event.event_id = new_event.event_id

    db.session.commit()

    return redirect('/gcal')


@app.route('/reports')
def display_reports():
    """Display user's reports."""

    user_id = session['user_id']
    goals = Goal.query.filter_by(user_id=user_id).order_by('name').all()
    categories = Category.query.filter_by(user_id=user_id).order_by(
        'name').all()

    time_periods = [('Last Week', 'last_week'), ('This Month', 'this_month'),
                    ('Last Month', 'last_month'), ('All Time', 'all_time')]

    return render_template("reports.html", goals=goals, categories=categories,
                           time_periods=time_periods)

@app.route('/report-goal-at-least-data')
def send_goal_at_least_data():
    """Sends data to client for displaying goal graph."""

    user_id = session['user_id']
    goals = Goal.query.filter_by(user_id=user_id, status='active', goal_type='at_least').order_by('name').all()
    categories = Category.query.filter_by(user_id=user_id).order_by(
        'name').all()

    goal_progress_data = {}

    for goal in goals:
        goal_progress_data[goal.name] = {
            "target": goal.duration.seconds / 3600,
            "total_time": goal.total_time("goal_time").seconds / 3600,
            "goal_type": goal.goal_type
        }

    print goal_progress_data

    goal_progress_data = jsonify(goal_progress_data)

    return goal_progress_data


@app.route('/report-goal-at-most-data')
def send_goal_at_most_data():
    """Sends data to client for displaying goal graph."""

    user_id = session['user_id']
    goals = Goal.query.filter_by(user_id=user_id, status='active', goal_type='at_most').order_by('name').all()
    categories = Category.query.filter_by(user_id=user_id).order_by(
        'name').all()


    goal_progress_data = {}

    for goal in goals:
        goal_progress_data[goal.name] = {
            "target": goal.duration.seconds / 3600,
            "total_time": goal.total_time("goal_time").seconds / 3600,
            "goal_type": goal.goal_type
        }

    print goal_progress_data

    goal_progress_data = jsonify(goal_progress_data)

    return goal_progress_data


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
