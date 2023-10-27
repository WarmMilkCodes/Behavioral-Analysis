import pymongo
import config
import certifi

MongoURL = config.client
ca = certifi.where()
cluster = pymongo.MongoClient(MongoURL, tlsCAFile=ca)
db = cluster[config.db]
students_collection = db[config.students_collection]
user_collection = db[config.user_collection]

def get_user_by_username(username):
    """
    Retrieve a user document from the database based on the username

    Parameters:
    - username (str): The username to search for

    Returns:
    - dict: The user document, if found, or None if not
    """
    user_data = user_collection.find_one({"username":username})
    return user_data