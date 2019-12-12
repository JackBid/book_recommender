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
static_dir = os.path.relpath('res/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = "secretkey"

recommender = Recommender()

# Create a new user profile when user enters page
user_id = recommender.newUserId()
user_profile = UserProfile(user_id)

@app.route('/', methods=['GET', 'POST'])
def home():

    form = RatingFormID()
    titles = None
    message = ''

    # If form has been submitted update the user profile
    if form.validate_on_submit():
        # Get form inputs
        book_title = form.book_title.data
        book_id = recommender.titleToBookId(book_title)
        rating = form.rating.data

        if book_id == -1:
            message = 'Sorry, we cannot find "' + str(book_title) + '" in our database.'
        elif rating <= 0 or rating > 5:
            message = 'Please enter a number 1-5 for rating.'
        else:
            recommender.rate(user_profile, book_id, rating, book_title)
        
    recommendedIds = collaborative_filter(user_profile.ratings, recommender.ratings_data, recommender.genre_data)
    titles = recommender.getTitlesFromBookIds(recommendedIds)

    if titles is None:
        return render_template('index.html', form=form, user_ratings=user_profile.ratings, message=message)
    
    return render_template('index.html', form=form, titles=titles, user_ratings=user_profile.ratings, message=message)

@app.route('/reset_profile')
def resetUserProfle():
    global user_profile
    user_id = recommender.newUserId()
    user_profile = UserProfile(user_id)
    return 'reset profile'

@app.route('/reset_rating')
def resetRating():
    index = request.args.get('index')

    try:
        index = int(index)
        print(index)
        user_profile.removeRating(index)
        return 'updated profile'
    except:
        return 'bad query string'

if __name__ == '__main__':
    app.run()