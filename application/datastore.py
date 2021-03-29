from google.cloud import datastore

datastore_client = datastore.Client()
user_query = datastore_client.query(kind='User')

def user_exists_login(user_id, password):
    user_query.add_filter('id', '=', user_id)
    user_query.projection = ["password"]

    if (user_query.fetch()):
        for user in user_query.fetch():
          if user['id'] == user_id and user['password'] == password:
            return True

    return False

def property_is_unique(property, user_input):
    try:
        user_query.projection = [property]

        if (user_query.fetch()):
            for user in user_query.fetch():
                if user[property] == user_input:
                    return True
    except:
        print("This property does not exist")

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
