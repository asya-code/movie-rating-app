"""CRUD operations."""

from model import db, datetime, User, Movie, Ratings, connect_to_db

#users

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)
    return user

def display_users():
    """return all users"""

    return User.query.all()

def display_emails():
    emails = []
    for user in display_users():
        emails.append(user.email)
    return emails

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()
    
#movies

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie"""

    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def display_movies():
    """return all movies"""
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """takes in a movie id and returns movie object"""

    return Movie.query.get(movie_id)



#ratings

def create_rating(score, user, movie):
    """Create new rating"""
    rating = Ratings(score=score, user = user, movie = movie)

    return rating

def get_rating(user_obj, movie_obj):
    """Takes in user object and movie object, returns rating by that user on that movie"""
    
    return Ratings.query.filter(Ratings.user == user_obj, Ratings.movie == movie_obj).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)