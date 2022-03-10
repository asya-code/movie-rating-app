"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


#generate movies to add to db

movies_list = []

for movie in movie_data:
    movie_to_add= crud.create_movie(movie['title'], 
    movie['overview'], 
    datetime.strptime(movie['release_date'], '%Y-%m-%d'), 
    movie['poster_path'])
    movies_list.append(movie_to_add)


#generate users and ratings to add to db

users_list = []
ratings_list = []

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    #declare a variable euqla to instance of User class with email and password
    user = crud.create_user(email,password)
    #append to users_list
    users_list.append(user)

    #10 reviews for each user
    for n in range(10):
        #create a rating using the create_rating fct
        rating = crud.create_rating(randint(1,5), user, choice(movies_list))
        #append it to the ratings_list
        ratings_list.append(rating)

#add all data to database
model.db.session.add_all(movies_list)
model.db.session.add_all(users_list)
model.db.session.add_all(ratings_list)
model.db.session.commit()

if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)