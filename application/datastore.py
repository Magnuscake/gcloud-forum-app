from datetime import datetime

from google.cloud import datastore

datastore_client = datastore.Client()

def user_exists_login(user_id, password):
    user_query = datastore_client.query(kind='User')
    user_query.add_filter('id', '=', user_id)
    user_query.projection = ['password', 'user_name']

    if (user_query.fetch()):
        for user in user_query.fetch():
            if user['password'] == password:
                return user['user_name'], user.key.id

    return None, None

def property_is_unique(property, user_input):
    user_query = datastore_client.query(kind='User')

    try:
        user_query.projection = [property]

        if (user_query.fetch()):
            for user in user_query.fetch():
                if user[property] == user_input:
                    return True
    except:
        print("This property does not exist")

    finally:
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

# TODO: Ancestor entities with id for key
# https://cloud.google.com/datastore/docs/concepts/entities#ancestor_paths
def create_new_message(subject, message_text, created_by, user_key):
    with datastore_client.transaction():
        message = datastore.Entity(datastore_client.key('User', user_key, 'Message'))

        now = datetime.now()

        message.update(
            {
                'created_by': created_by,
                'subject': subject,
                'message_text': message_text,
                'posted_on': datetime.utcnow(),
                'posted_on_formatted': now.strftime("%d/%m/%y, %I:%M %p")
            }
        )

        datastore_client.put(message)

def get_all_messages():
    message_query = datastore_client.query(kind='Message')
    message_query.order = ['-posted_on']
    message_query.projection = ['subject', 'message_text', 'posted_on_formatted', 'created_by']

    messages = message_query.fetch(limit=10)

    return messages

def get_user_messages(user_key):
    ancestor = datastore_client.key('User', user_key)
    message_query = datastore_client.query(kind='Message', ancestor=ancestor)

    message_query.order = ['-posted_on']
    message_query.projection = ['subject', 'message_text', 'posted_on_formatted']

    messages = message_query.fetch()

    return messages

def update_password(user_id, old_password, new_password):
    user_query = datastore_client.query(kind='User')
    user_query.add_filter('id', '=', user_id)

    for user in user_query.fetch():
        print(user.key.id)
        if user['password'] == old_password:
            with datastore_client.transaction():
                key = datastore_client.key('User', user.key.id)
                user_acc = datastore_client.get(key)

                user_acc['password'] = new_password

                datastore_client.put(user_acc)

                return True

    return False
