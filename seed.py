"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Category, Event, Task, Goal, GoalCategory
from datetime import datetime, date

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from user.txt into database."""

    print "Seeding users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/user.txt"):
        row = row.rstrip()
        user_id, name, email, password = row.split("|")

        user = User(user_id=user_id, name=name, email=email, password=password)

        db.session.add(user)

    db.session.commit()


def load_goals():
    """Load goals from goal.txt into database."""

    print "Seeding goals"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Goal.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/goal.txt"):
        row = row.rstrip()
        goal_id, name, start_time, end_time, goal_type, duration, \
            status, user_id = row.split("|")

        goal = Goal(goal_id=goal_id, start_time=start_time,
                    end_time=end_time, name=name, goal_type=goal_type,
                    duration=duration, status=status, user_id=user_id)

        db.session.add(goal)

    db.session.commit()


def load_categories():
    """Load goals from goal.txt into database."""

    print "Seeding categories"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Category.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/category.txt"):
        row = row.rstrip()
        category_id, name, user_id, status = row.split("|")

        category = Category(category_id=category_id,
                            name=name, status=status,
                            user_id=user_id)

        db.session.add(category)

    db.session.commit()


def load_goals_categories():
    """Load goals from goal.txt into database."""

    print "Seeding goals_categories"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    GoalCategory.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/goal_category.txt"):
        row = row.rstrip()
        goal_category_id, goal_id, category_id = row.split("|")

        goal_category = GoalCategory(goal_category_id=goal_category_id,
                                     goal_id=goal_id, category_id=category_id)

        db.session.add(goal_category)

    db.session.commit()


def load_tasks():
    """Load goals from goal.txt into database."""

    print "Seeding tasks"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Task.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/task.txt"):
        row = row.rstrip()
        task_id, name, category_id, user_id = row.split("|")

        task = Task(task_id=task_id, name=name,
                    category_id=category_id, user_id=user_id)

        db.session.add(task)

    db.session.commit()


def load_events():
    """Load goals from goal.txt into database."""

    print "Seeding events"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Event.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/event.txt"):
        row = row.rstrip()
        event_id, start_time, stop_time, user_id, task_id \
            = row.split("|")

        event = Event(event_id=event_id, start_time=start_time,
                      stop_time=stop_time, user_id=user_id,
                      task_id=task_id, status='active')

        db.session.add(event)

    db.session.commit()


class_list = [(User.user_id, 'user_id'),
              (Goal.goal_id, 'goal_id'),
              (Category.category_id, 'category_id'),
              (GoalCategory.goal_category_id, 'goal_category_id'),
              (Task.task_id, 'task_id'),
              (Event.event_id, 'event_id')]


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})

    # Get the Max goal_id in the database
    result = db.session.query(func.max(Goal.goal_id)).one()
    max_id = int(result[0])

    # Set the value for the next goal_id to be max_id + 1
    query = "SELECT setval('goals_goal_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})

    # Get the Max category_id in the database
    result = db.session.query(func.max(Category.category_id)).one()
    max_id = int(result[0])

    # Set the value for the next category_id to be max_id + 1
    query = "SELECT setval('categories_category_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})

    # Get the Max goal_category_id in the database
    result = db.session.query(func.max(GoalCategory.goal_category_id)).one()
    max_id = int(result[0])

    # Set the value for the next goal_category_id to be max_id + 1
    query = "SELECT setval('goals_categories_goal_category_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})

    # Get the Max task_id in the database
    result = db.session.query(func.max(Task.task_id)).one()
    max_id = int(result[0])

    # Set the value for the next task_id to be max_id + 1
    query = "SELECT setval('tasks_task_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})

    # Get the Max event_id in the database
    result = db.session.query(func.max(Event.event_id)).one()
    max_id = int(result[0])

    # Set the value for the next event_id to be max_id + 1
    query = "SELECT setval('events_event_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})









    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_goals()
    load_categories()
    load_goals_categories()
    load_tasks()
    load_events()
    set_val_user_id()
