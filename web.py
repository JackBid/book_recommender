import os
import pandas as pd

from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask import request

from config import Config
from forms.ratingForms import RatingFormID
from user_profile import UserProfile
from recommender import Recommender
from collaborative_filtering import collaborative_filter

template_dir = os.path.relpath('res/templates')

app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = "secretkey"

recommender = Recommender()

# Create a new user profile when user enters page
user_id = recommender.newUserId()
user_profile = UserProfile(user_id)

@app.route('/', methods=['GET', 'POST'])
def home():

    form = RatingFormID()
    titles = None

    # If form has been submitted
    if form.validate_on_submit():
        # Get form inputs
        book_id = form.book_id.data
        rating = form.rating.data

        recommender.rate(user_profile, book_id, rating)
        recommendedIds = collaborative_filter(user_profile.ratings, recommender.ratings_data, recommender.genre_data)

        titles = recommender.getTitlesFromBookIds(recommendedIds)

    if titles is None:
        return render_template('index.html', form=form)
    
    return render_template('index.html', form=form, titles=titles)



if __name__ == '__main__':
    app.run()