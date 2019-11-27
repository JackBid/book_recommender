import numpy as np
import pandas as pd 

pd.set_option('display.max_columns', None)

def getGenreData():
    
    book_data = pd.read_csv('res/books.csv')
    book_tag_data = pd.read_csv('res/book_tags.csv')
    tag_data = pd.read_csv('res/tags.csv')

    genres_full = pd.merge(book_tag_data, tag_data, on='tag_id')

    a = book_data[['book_id', 'goodreads_book_id', 'original_title']].head()
    genres_full = pd.merge(genres_full, a, on='goodreads_book_id')

    genres = genres_full[['book_id', 'original_title', 'tag_name']]

    return genres

ratings_data = pd.read_csv('res/ratings.csv')
genre_data = getGenreData()

def newUserId():
    return ratings_data['user_id'].max() + 1
    
def rate(user_id, book_id, rating):

    global ratings_data

    user_id_indicies = ratings_data.user_id[ratings_data['user_id'] == user_id].index.tolist()

    for index in user_id_indicies:
        if ratings_data.iloc[index][1] == book_id:
            ratings_data.iloc[index][2] = rating
            return

    ratings_data = ratings_data.append({'user_id': user_id, 'book_id': book_id, 'rating': rating}, ignore_index=True)

print(ratings_data.head())

rate(2, 2318, 5)

print(ratings_data.head())
'''
print('\n')
print(genre_data.head())'''

