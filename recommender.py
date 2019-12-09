import numpy as np
import pandas as pd 

from user_profile import UserProfile

pd.set_option('display.max_columns', None)

'''
Generate the correct data tables
'''
def getGenreData():
    
    book_data = pd.read_csv('res/books.csv')
    book_tag_data = pd.read_csv('res/book_tags.csv')
    tag_data = pd.read_csv('res/tags.csv')

    genres_full = pd.merge(book_tag_data, tag_data, on='tag_id')

    a = book_data[['book_id', 'goodreads_book_id', 'original_title']].head()
    genres_full = pd.merge(genres_full, a, on='goodreads_book_id')

    genres = genres_full[['book_id', 'original_title', 'tag_name']]

    return genres

'''
Create a new unique user ID
'''
def newUserId():
    return ratings_data['user_id'].max() + 1

'''
Given a user, book_id and rating update the rating table and the user_profile ratings
'''
def rate(user, book_id, rating):

    user_id = user.id
    global ratings_data

    # Get the indicies of books the user has rated
    user_id_indicies = ratings_data.user_id[ratings_data['user_id'] == user_id].index.tolist()

    # If already rated, update the user rating
    for index in user_id_indicies:
        if ratings_data.iloc[index][1] == book_id:
            ratings_data.iloc[index][2] = rating
            return
        
    # Add a new rating
    ratings_data = ratings_data.append({'user_id': user_id, 'book_id': book_id, 'rating': rating}, ignore_index=True)

    # Update the user profile rating list
    user.ratings.append({'user_id': user_id, 'book_id': book_id, 'rating': rating})

# Create the tables 
ratings_data = pd.read_csv('res/ratings.csv')
genre_data = getGenreData()

print(ratings_data.head())

# Create a new user profile and add a rating
i = newUserId()
jack = UserProfile(i)
rate(jack, 2318, 5)

print(ratings_data.head())
print(jack.ratings)
