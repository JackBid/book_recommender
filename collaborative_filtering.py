import pandas as pd

'''
Takes a list of user ratings, a list of rating data and genre data
and returns a list of ratings
'''
def collaborative_filter(user_ratings, ratings_data, genre_data):

    ''' 
    1. Which users had similar ratings?
    '''
    similar_users = []
    
    # Select users that gave the book the same rating
    for user_rating in user_ratings:
        rows = ratings_data[(ratings_data['book_id'] == user_rating['book_id']) & (ratings_data['rating'] == user_rating['rating'])]
        similar_users.extend(rows['user_id'].tolist())

    '''
    2. What did similar users also like?
    '''

    recommended_books = {}
    book_ids = []


    for i in range(0, len(similar_users), 150):
        book_ids.extend(ratings_data[(ratings_data['user_id'] == similar_users[i]) & (ratings_data['rating'] == 5)]['book_id'].tolist())

    for book_id in book_ids:
        if book_id in recommended_books:
            recommended_books[book_id] += 1
        else:
            recommended_books[book_id] = 1

    '''
    3. Sort the recommendations by how many users also had them and remove ones already in recs
    '''

    sorted_recommendation = sorted(recommended_books.items(), key=lambda item: item[1])[-20:]
    unique_recommendations = []

    for recommendation in sorted_recommendation:
        for rating in user_ratings:
            if recommendation[0] != user_rating['rating']:
                unique_recommendations.append(recommendation[0])

    return unique_recommendations