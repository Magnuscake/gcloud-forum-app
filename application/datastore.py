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

    user_query.projection = [property]

    for user in user_query.fetch():
        if user[property] == user_input:
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

def create_new_message(subject, message_text, created_by, user_key, img_url):
    with datastore_client.transaction():
        message = datastore.Entity(datastore_client.key('User', user_key, 'Message'))

        now = datetime.now()

        message.update(
            {
                'created_by': created_by,
                'subject': subject,
                'message_text': message_text,
                'posted_on': datetime.utcnow(),
                'posted_on_formatted': now.strftime("%d/%m/%y, %I:%M %p"),
                'img_url': img_url
            }
        )

        datastore_client.put(message)

def get_all_messages():
    message_query = datastore_client.query(kind='Message')
    message_query.order = ['-posted_on']
    message_query.projection = ['subject', 'message_text', 'posted_on_formatted', 'created_by', 'img_url']

    messages = message_query.fetch(limit=10)

    return messages

def get_user_messages(user_key):
    ancestor = datastore_client.key('User', user_key)
    message_query = datastore_client.query(kind='Message', ancestor=ancestor)

    message_query.order = ['-posted_on']
    message_query.projection = ['subject', 'message_text', 'posted_on_formatted', 'img_url']

    messages = message_query.fetch()

    return messages

def get_single_message(message_key, user_key):
    message_key = datastore_client.key('User', int(user_key), 'Message', int(message_key))
    message = datastore_client.get(message_key)

    return message

def update_password(user_id, old_password, new_password):
    user_key = datastore_client.key('User', int(user_id))
    user = datastore_client.get(user_key)

    if (old_password == user['password']):
        user['password'] = new_password

        datastore_client.put(user)
        return True

    return False

def update_message(message_key, user_key, username, img_url, subject, message_text):
    key = datastore_client.key('User', int(user_key), 'Message', int(message_key))

    #  message = datastore_client.get(key)
    message = datastore.Entity(key=key)

    now = datetime.now()

    #  message['subject'] = subject
    #  message['message_text'] = message_text
    #  message['posted_on'] = datetime.utcnow(),
    #  message['posted_on_formatted'] = now.strftime("%d/%m/%y, %I:%M %p"),


    message.update(
        {
            'subject': subject,
            'message_text': message_text,
            'created_by': username,
            'img_url': img_url,
            'posted_on': datetime.utcnow(),
            'posted_on_formatted': now.strftime("%d/%m/%y, %I:%M %p"),
        }
    )

    datastore_client.put(message)
