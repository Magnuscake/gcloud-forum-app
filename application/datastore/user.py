from google.cloud import datastore

datastore_client = datastore.Client()

def user_exists(user_id, password):
    query = datastore_client.query(kind='User')
    #  query.order = ['user_name']
    query.projection = ["id", "password", "user_name"]

    for user in query.fetch():
        if user['id'] == user_id and user['password'] == password:
            return True

    return False
