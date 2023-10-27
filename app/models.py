import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import dbInfo
from dbInfo import get_user_by_username

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

    @staticmethod
    def authenticate(username, password):
        user_data = get_user_by_username(username)
        if user_data and check_password_hash(user_data['password'], password):
            return User(username, user_data['password'])
        return None
    
    @staticmethod
    def create_user(username, password):
        hashed_pwd = generate_password_hash(password, method='sha256')
        dbInfo.user_collection.insert_one({"username":username, "password":hashed_pwd})

# Dummy dataset for training
X_train =  [
    # Sample data: attendance, average score
    [95, 85],
    [80, 70],
    [60, 50],
]

y_train = ['Highly Engaged', 'Moderately Engaged', 'Low Engagement']

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

def predict_engagement(data):
    prediction = clf.predict([[data['attendance'], data['average_score']]])
    return prediction[0]