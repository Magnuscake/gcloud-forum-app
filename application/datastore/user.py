from google.cloud import datastore

datastore_client = datastore.Client()

def user_exists(user_id, password):
    # TODO: Implement cleaner way to access db
    query = datastore_client.query(kind='User')
    #  query.order = ['user_name']
    query.projection = ["id", "password", "user_name"]

    for user in query.fetch():
        if user['id'] == user_id and user['password'] == password:
            return True

    return False

def create_new_user(user_id, username, password):
    user = datastore.Entity(datastore_client.key('User'))
    user.update(
        {
            "id": user_id,
            "user_name": username,
            "password": password
        }
    )

    datastore_client.put(user)
