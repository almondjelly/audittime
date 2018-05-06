"""Auditime server."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Category, Event, Task, Goal, \
                  GoalCategory
from datetime import datetime
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
        return "success"

    except:
        return "fail"


@app.route('/logout', methods=['POST'])
def logout():
    """Log user out of session."""

    session.pop('user')

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

    return redirect('/')


@app.route('/user')
def userhome():
    """Display user's unique homepage."""

    return render_template("userhome.html")


@app.route('/start_stopwatch', methods=['POST'])
def grab_start_time():
    """Grabs start time."""

    session['start_time'] = datetime.now()
    session['task'] = request.form.get('task')
    session['category'] = request.form.get('category')

    return redirect('/user')


@app.route('/add_event', methods=['POST'])
def add_event():
    """Adds a new event to the database and returns its duration."""

    start_time = session['start_time']
    stop_time = datetime.now()
    task_name = session['task']
    category_name = session['category']
    user_id = User.query.filter_by(email=session['user']).one().user_id

    # # If the task already exists, find its id.
    if Task.query.filter_by(name=task_name).first():
        task_id = Task.query.filter_by(name=task_name).first().task_id

    else:
    #     # Create a new task.
    #     # If the category already exists, find its id.
        if Category.query.filter_by(name=category_name).first():
            category_id = Category.query.filter_by(name=category_name) \
                .first().category_id

        else:
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

    #     # Find the newly created task's id.
        task_id = Task.query.filter_by(name=task_name).first().task_id
        task_id = new_task.task_id

    # # With the task_id, we now have enough info to create the new event.
    # new_event = Event(start_time=start_time, stop_time=stop_time,
    #                   user_id=user_id, task_id=task_id)

    db.session.add(new_event)
    db.session.commit()

    return redirect('/user')


# @app.route('/')
# def index():
#     """Homepage."""

#     try:
#         if request.args.get("logout") == 'logout':
#             del session['user_id']
#             flash("You've logged out :(")
#             return redirect('/')

#         else:
#             return render_template("homepage.html")

#     except:
#         flash("You haven't logged in yet, dummy!")
#         return redirect('/')


# @app.route('/movies')
# def movie_list():
#     """SHOW ME THOSE MOVIES"""

#     movie_list = Movie.query.order_by('title').all()
#     return render_template("movies.html", movie_list=movie_list)


# @app.route('/movies/<movie_id>')
# def movie_page(movie_id):
#     """Show details about a specific movie.
#     If a user is logged in, let them add/edit a rating."""

#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Ratings.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

#     # Get average rating of movie
#     rating_scores = [r.score for r in movie.ratings]
#     avg_rating = float(sum(rating_scores)) / len(rating_scores)

#     # Prediction code: only predict if the user hasn't rated it.
#     prediction = None

#     if (not user_rating) and user_id:
#         user = User.query.get(user_id)
#         if user:
#             prediction = user.predict_rating(movie)

#     # Either use the prediction or their real rating
#     if prediction:
#         # User hasn't scored; use our prediction if we made one
#         effective_rating = prediction

#     elif user_rating:
#         # User has already scored for real; use that
#         effective_rating = user_rating.score

#     else:
#         # User hasn't scored, and we couldn't get a prediction
#         effective_rating = None

#     # Get the eye's rating, either by predicting or using real rating

#     the_eye = (User.query.filter_by(email="the-eye@of-judgment.com")
#                          .all()[1])
#     eye_rating = Ratings.query.filter_by(
#         user_id=the_eye.user_id, movie_id=movie.movie_id).first()

#     if eye_rating is None:
#         eye_rating = the_eye.predict_rating(movie)
#         print 'eye rating!', eye_rating

#     else:
#         eye_rating = eye_rating.score

#     if eye_rating and effective_rating:
#         difference = abs(eye_rating - effective_rating)

#     else:
#         # We couldn't get an eye rating, so we'll skip difference
#         difference = None
#         print 'no difference :('

#     # Depending on how different we are from the Eye, choose a
#     # message

#     BERATEMENT_MESSAGES = [
#         "I suppose you don't have such bad taste after all.",
#         "I regret every decision that I've ever made that has " +
#         "brought me to listen to your opinion.",
#         "Words fail me, as your taste in movies has clearly " +
#         "failed you.",
#         "That movie is great. For a clown to watch. Idiot.",
#         "Words cannot express the awfulness of your taste."
#     ]

#     if difference:
#         beratement = BERATEMENT_MESSAGES[int(difference)]

#     else:
#         beratement = None
#         print 'no beratement :('

#     all_movie_data = db.session.query(Movie.title,
#                                       Movie.release_date,
#                                       Movie.imdb_url,
#                                       Movie.movie_id,
#                                       Ratings.user_id,
#                                       Ratings.score
#                                       ).filter_by(movie_id=movie_id
#                                                   ).join(Ratings).all()

#     # check if user is logged in
#     try:
#         if session['user_id']:
#             login_yesno = "true"
#     except:
#         login_yesno = "false"

#     return render_template("movie_details.html",
#                            all_movie_data=all_movie_data,
#                            login_yesno=login_yesno,
#                            user_rating=user_rating,
#                            average=avg_rating,
#                            prediction=prediction,
#                            beratement=beratement)


# @app.route('/display_rating')
# def display_rating():
#     """Display that rating, yo!"""

#     movie_id = request.args.get("movie_id")

#     # queries database (ratings table) for object, filtered on movie and user
#     user_rating = db.session.query(Ratings.score).filter_by(movie_id=movie_id, user_id=session['user_id']).all()

#     # jsonified user_rating is passed into displayRateOption()
#     return jsonify(user_rating)


# @app.route('/add-rating', methods=['POST'])
# def add_rating():
#     """Add or update user rating for a movie."""

#     # grabs new_rating & movie_id values from incoming post request sent by addRating
#     # function on the html side
#     new_rating = request.form.get('new_rating')
#     movie_id = request.form.get('movie_id')
#     # queries database (ratings table) for object, filtered on movie and user
#     user_rating = Ratings.query.filter_by(movie_id=movie_id, user_id=session['user_id']).first()
#     if user_rating:
#         # updates user's score with the new rating
#         user_rating.score = new_rating

#     # if user has not rated the movie yet, then create a new row in the Ratings
#     else:
#         new_rating_object = Ratings(user_id=session['user_id'],
#                                     movie_id=movie_id,
#                                     score=new_rating
#                                     )
#         db.session.add(new_rating_object)
#     db.session.commit()

#     # new_rating is passed into updateRating()
#     return new_rating


# @app.route('/users')
# def user_list():
#     """SHOW ME THOSE USERS"""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route('/users/<user_id>')
# def user_page(user_id):
#     """Display information about an individual user."""

#     user_info = User.query.filter_by(user_id=user_id).first()
#     user_ratings = db.session.query(Ratings.score,
#                                     Movie.title,
#                                     Movie.movie_id,
#                                     Movie.imdb_url
#                                     ).filter_by(user_id=user_id).join(Movie).order_by('title').all()

#     return render_template("user_page.html", user_info=user_info, user_ratings=
#                            user_ratings)


# @app.route('/register', methods=['GET'])
# def register_form():
#     """Displays the registration and login form."""

#     return render_template("register_form.html")


# @app.route('/register', methods=['POST'])
# def register_process():
#     """Register users who don't have an account yet OR logs in users
#     who are already in the db."""

#     user_email = request.form.get('email')
#     user_pw = request.form.get('password')

#     # check that email is in users table
#     if User.query.filter_by(email=user_email).first():

#         # if so, store the user's id in queried_id
#         queried_id = User.query.filter_by(email=user_email).first().user_id

#         # check that the password is correct
#         if User.query.filter_by(email=user_email).first().password == user_pw:

#             # if password matches, store the user's id in the flask session; log them in
#             session["user_id"] = queried_id

#             #FLASH TEXT TO CONFIRM LOGIN
#             flash("You've successfully logged in! Hoorayyyyy!")
#             return redirect("/")

#         # if password doesn't match, alert the user that their password is wrong
#         else:
#             flash("That password is not correct. Try again!")
#             return redirect("/register")

#     # if the email doesn't already exist in the table, create new user
#     else:
#         db.session.add(User(email=user_email, password=user_pw))
#         db.session.commit()
#         # add queried_id to session, log them in
#         queried_id = User.query.filter_by(email=user_email).first().user_id
#         session["user_id"] = queried_id

#         # FLASH TEXT TO CONFIRM ACCOUNT CREATION + LOGIN
#         flash("You've successfully created your account! You're now logged in!")
#         return redirect("/")


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
