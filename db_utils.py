from tinydb import TinyDB
from formFinder import app

FORMS = [
    {'name': 'login_form',
     'fields': [{'name': 'username', 'type': 'text'},
                {'name': 'password', 'type': 'text'}]},
    {'name': 'user_info_form',
     'fields': [{'name': 'username', 'type': 'text'},
                {'name': 'user_email', 'type': 'email'},
                {'name': 'user_phone', 'type': 'phone'},
                {'name': 'birthday', 'type': 'date'}]},
    {'name': 'send_email_form',
     'fields': [{'name': 'recipient', 'type': 'text'},
                {'name': 'rec_email', 'type': 'email'},
                {'name': 'message', 'type': 'text'}]}
]


def init_db(db_path):
    db = TinyDB(db_path)
    for form in FORMS:
        db.insert(form)
    return db


if __name__ == '__main__':
    init_db(app.config['DATABASE'])
