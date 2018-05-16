"""Auditime server."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Category, Event, Task, Goal, \
                  GoalCategory
from datetime import datetime, timedelta
from addNew import goal_generate_html, category_generate_html
from math import floor
import json
import pdb


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Display homepage."""

    return render_template('index.html')


@app.route('/signin', methods=['POST'])
def signin():
    """Collect login information."""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        if User.query.filter_by(email=email).one().password == password:
            session['user'] = email
            session['user_id'] = User.query.filter_by(
                email=email).one().user_id

        return "success"

    except:
        return "fail"


@app.route('/logout', methods=['POST'])
def logout():
    """Log user out of session."""

    session.pop('user')
    session.pop('user_id')

    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    """Registers user and adds them to the users table."""

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User(name=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    session['user'] = email
    session['user_id'] = User.query.filter_by(email=email).one().user_id

    return redirect('/')


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

    new_goal = Goal(name=goal_name, start_time=start_time, end_time=end_time,
                    goal_type=goal_type, duration=duration, status="Active",
                    user_id=user_id)

    db.session.add(new_goal)
    db.session.commit()

    goal = Goal.query.filter_by(name=goal_name, end_time=end_time,
                                user_id=user_id).one()

    goal_id = str(goal.goal_id)
    goal_category = goal.category
    total_time = goal.total_time()

    categories = Category.query.filter_by(user_id=user_id).all()

    new_goal_html = goal_generate_html(total_time, goal_id, goal_name,
                                       goal_type,
                                       duration.days, str(hours), str(minutes),
                                       start_time, end_time, categories,
                                       goal_category)

    return new_goal_html


@app.route('/add_category', methods=['POST'])
def add_category():
    """Adds a category to the categories table."""

    # Grab data from form via JavaScript
    category_name = request.form.get('categoryName')
    category_goals = request.form.getlist('categoryGoals')
    user_id = session['user_id']

    # Add new category to the categories table.
    new_category = Category(name=category_name, user_id=user_id)
    db.session.add(new_category)
    db.session.commit()

    # # Add new goal associations to the goals_categories table.
    category_id = Category.query.filter_by(name=category_name,
                                           user_id=user_id).one().category_id

    for goal_name in category_goals:
        goal_id = Goal.query.filter_by(name=goal_name, user_id=user_id).one(
            ).goal_id

        new_goal_category = GoalCategory(goal_id=goal_id,
                                         category_id=category_id)
        db.session.add(new_goal_category)

    db.session.commit()

    # Grab data required for generating relevant html.
    all_goals = Goal.query.all()
    category_goal = Category.query.filter_by(category_id=category_id).one(
        ).goal

    new_category_html = category_generate_html(category_id, category_name,
                                               all_goals, category_goal)

    return new_category_html


@app.route('/goals')
def display_goals():
    """Displays user's goals."""

    goals = db.session.query(Goal).filter_by(
        user_id=session['user_id']).order_by(
        'end_time').all()

    categories = db.session.query(Category).filter_by(
        user_id=session['user_id']).order_by(
        'name').all()

    return render_template("goals.html", goals=goals,
                           categories=categories)


@app.route('/edit_goal_info', methods=['POST'])
def edit_goal_info():
    """Updates new goal info in the goals table."""

    goal_id = request.form.get('goalId')
    new_goal_name = request.form.get('newGoalName')
    new_days = int(request.form.get('newDays'))
    new_hours = int(request.form.get('newHours'))
    print new_hours, "new hours"
    new_minutes = int(request.form.get('newMinutes'))
    new_duration = timedelta(days=new_days, hours=new_hours, minutes=new_minutes)

    # Find the existing goal.
    goal = Goal.query.filter_by(goal_id=goal_id).one()

    # Update name and duration.
    goal.name = new_goal_name
    goal.duration = new_duration

    db.session.commit()

    flash("goal updated ")

    print goal

    return redirect('/user')


@app.route('/user')
def userhome():
    """Display user's unique homepage: stopwatch, manual entry, task log."""

    categories = db.session.query(Category).filter_by(
        user_id=session['user_id']).order_by('name').all()

    events = db.session.query(Event).filter_by(
        user_id=session['user_id']).order_by('stop_time').all()

    # Display log in reverse chronological order.
    events.reverse()

    return render_template("userhome.html", events=events,
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
    user_id = User.query.filter_by(email=session['user']).one().user_id

    # If the task already exists, find its id.
    if Task.query.filter_by(name=task_name).first():
        task_id = Task.query.filter_by(name=task_name).first().task_id

    else:
        # Create a new task.
        # If the category already exists, find its id.
        try:
            if int(Category.query.filter_by(name=category_name).first().user_id) \
                    == int(user_id):
                category_id = Category.query.filter_by(name=category_name) \
                    .first().category_id

        except:
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
                      user_id=user_id, task_id=task_id)

    db.session.add(new_event)
    db.session.commit()

    event = Event.query.filter_by(task_id=task_id, stop_time=stop_time).one()

    form_html = "<li> \
        <form> \
            <!-- Task --> \
            <span class=\"task-input\"> \
                <span class=\"event-{event_id}\"> \
                    <input type=\"text\" value=\"{task_name}\" name=\"{event_id2}\" class=\"input-field\"> \
                </span> \
            </span> \
\
            <!-- Category --> \
            <span class=\"category-title\"> \
                <span class=\"event-{event_id3}\"> \
                    {category_name} \
\
                    <!-- Dropdown for multiple selecting categories --> \
                    <div class=\"category-dropdown event-{event_id4}\"> \
                    <!-- ADD THE ACTUAL OPTIONS FOR PICKING CATEGORIES OR SOMETHING --> \
                        <ul> \
                            <li>asdf1</li> \
                            <li>asdf2</li> \
                            <li>asdf3</li> \
                        </ul> \
                    </div> \
                </span> \
            </span> \
\
            <!-- Duration --> \
            <span>{duration}</span> \
            <!-- Save --> \
            <span class=\"event-edit-submit {event_id5}Submit\">save</span> \
        </form> \
    </li>".format(event_id=event.event_id,
                  task_name=event.task.name,
                  event_id2=event.event_id,
                  event_id3=event.event_id,
                  category_name=event.task.category.name,
                  event_id4=event.event_id,
                  duration=event.duration(),
                  event_id5=event.event_id
                  )

    return form_html


@app.route('/edit_task_name', methods=['POST'])
def edit_task_name():
    """Updates new task name in the tasks table."""

    event_id = request.form.get('eventId')
    new_task_name = request.form.get('newTaskName')
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
    Event.query.filter_by(event_id=event_id).one().task_id = new_task_id

    db.session.commit()

    flash("task updated")

    return redirect('/user')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
