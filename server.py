"""Server for movie ratings app."""

from flask import (Flask, render_template, render_template_string, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_homepage():
    """shows homepage"""
    return render_template("homepage.html")

@app.route('/movies')
def all_movies():
    """view all movies"""

    movies = crud.display_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """displays the details of a movie"""

    movie_obj = crud.get_movie_by_id(movie_id)

    return render_template(f'movie_details.html', movie=movie_obj)

@app.route("/rate/<movie_id>", methods=["POST"])
def add_rating(movie_id):

    movie_obj = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_id(session['current_user'])
    rating = request.form.get("rating")
    print(session['current_user'])

    #if there is already a rating by current user on this movie:
        #then update the rating with the new rating


    #if there isn't already one:
        #then create a new rating and add it

    current_rating = crud.get_rating(user_obj=user, movie_obj=movie_obj)
    if current_rating:
        current_rating.score = rating #updates the score attribute of this object
    else:
        new_rating = crud.create_rating(score=rating, user=user, movie=movie_obj)
        db.session.add(new_rating)

    db.session.commit()
    flash("Thank you!")
    return redirect(f"/movies/{movie_id}")

@app.route('/users')
def show_users():
    """displays users list"""
    users = crud.display_users()
    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """displays user info"""

    #user obj by id
    user = crud.get_user_by_id(user_id)
    return render_template('user_details.html', user=user)


@app.route('/user_registration', methods=["POST"])
def register_user():
    """create an account"""
    #assign email and password variables with request.form.get
    email = request.form.get("email")
    password = request.form.get("password")
    
    if crud.get_user_by_email(email):
        flash("This user already exists, please, log in")    
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Welcome, new user!")

    return redirect('/')

@app.route("/login", methods=["POST"])
def log_in():
    login_email = request.form.get("email")
    login_password = request.form.get("password")
    if crud.get_user_by_email(login_email):

        user = crud.get_user_by_email(login_email)
        if login_password != user.password:
            flash("Incorrect password. Try again")
        else:
            #add the user's user_id to the flask session
            session['current_user'] = user.user_id
            session['current_email'] = user.email
            session['current_user_obj'] = user
            flash(f'Logged in as {user.email}')
    else:
        flash("Looks like we don't know you yet! ")

    return redirect("/")



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
