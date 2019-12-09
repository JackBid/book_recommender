import os
import pandas as pd

from flask import Flask
from flask import render_template

from user_profile import UserProfile
from recommender import Recommender
from collaborative_filtering import collaborative_filter


app = Flask(__name__)

template_dir = os.path.relpath('res/templates')
app = Flask(__name__, template_folder=template_dir)

recommender = Recommender()

@app.route('/')
def home():

    # Create a new user profile when user enters page
    user_id = recommender.newUserId()
    user_profile = UserProfile(user_id)

    # Give a book a rating
    book_id = 50
    rating = 5
    recommender.rate(user_profile, book_id, rating)

    recommendedIds = collaborative_filter(user_profile.ratings, recommender.ratings_data, recommender.genre_data)

    titles = recommender.getTitlesFromBookIds(recommendedIds)

    return render_template('index.html', titles=titles)

if __name__ == '__main__':
    app.run()