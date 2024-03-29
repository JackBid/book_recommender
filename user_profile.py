class UserProfile():
    def __init__(self, id):
        self.ratings = []
        self.id = id

    def addRating(self, rating):
        self.ratings.append(rating)

    def addRating(self, book_id, rating, title):
        self.ratings.append({'user_id': self.id, 'book_id': book_id, 'rating': rating, 'title': title})     

    def updateRating(self, book_id, rating):
        for user_rating in self.ratings:
            if user_rating['book_id'] == book_id:
                user_rating['rating'] = rating

    def removeRating(self, index):
        del self.ratings[index]