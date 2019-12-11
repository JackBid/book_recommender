import numpy as np
import pandas as pd 

from user_profile import UserProfile
from collaborative_filtering import collaborative_filter

pd.set_option('display.max_columns', None)

class Recommender():
    
    def __init__(self):
        
        self.ratings_data = pd.read_csv('res/bookData/ratings.csv')
        self.genre_data = self.getGenreData()

    '''
    Generate the correct data tables
    '''
    def getGenreData(self):
        
        book_data = pd.read_csv('res/bookData/books.csv', )
        book_tag_data = pd.read_csv('res/bookData/book_tags.csv')
        tag_data = pd.read_csv('res/bookData/tags.csv')

        book_tag_data.set_index('tag_id', inplace=True)
        tag_data.set_index('tag_id', inplace=True)
        genres_full = book_tag_data.join(tag_data, how='left')

        a = book_data[['book_id', 'goodreads_book_id', 'original_title']]

        a.set_index('goodreads_book_id', inplace=True)
        genres_full.set_index('goodreads_book_id', inplace=True)
        genres_full = a.join(genres_full, how='left')

        genres = genres_full[['book_id', 'original_title', 'tag_name']]

        return genres

    '''
    Create a new unique user ID
    '''
    def newUserId(self):
        return self.ratings_data['user_id'].max() + 1

    '''
    Given a user, book_id and rating update the rating table and the user_profile ratings
    '''
    def rate(self, user, book_id, rating, title):

        user_id = user.id

        # Get the indicies of books the user has rated
        user_id_indicies = self.ratings_data.user_id[self.ratings_data['user_id'] == user_id].index.tolist()

        # If already rated, update the user rating
        for index in user_id_indicies:
            # Updte user profile
            if self.ratings_data.iloc[index][0] == user_id:
                user.updateRating(book_id, rating)
            
            # Update ratings table
            if self.ratings_data.iloc[index][1] == book_id:
                self.ratings_data.iloc[index][2] = rating
                return
            
        # Add a new rating
        self.ratings_data = self.ratings_data.append({'user_id': user_id, 'book_id': book_id, 'rating': rating}, ignore_index=True)

        # Update the user profile rating list
        user.ratings.append({'user_id': user_id, 'book_id': book_id, 'rating': rating, 'title': title})

    def titleToBookId(self, title):
        try:
            row = self.genre_data[self.genre_data['original_title'] == title].iloc[0]
        except:
            return -1
        return row.get(key = 'book_id')

    def idToBookTitle(self, id):
        try:
            row = self.genre_data[self.genre_data['book_id'] == id].iloc[0]
        except:
            return -1
        return row.get(key = 'original_title')

    def getTitlesFromBookIds(self, bookIds):

        titles = []

        for book_id in bookIds:
            row = self.genre_data[self.genre_data['book_id'] == book_id].iloc[0]
            titles.append(row.get(key = 'original_title'))

        return titles

'''
user = UserProfile(recommender.newUserId)

recommender.rate(user, 100, 5)

ids = collaborative_filter(user.ratings, recommender.ratings_data, recommender.genre_data)

print(recommender.getTitlesFromBookIds(ids))'''
