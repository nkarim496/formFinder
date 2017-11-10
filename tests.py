import os
import formFinder as ff
import unittest
import tempfile
from db_utils import init_db


class FormFinderTestCase(unittest.TestCase):
    def setUp(self):
        self.db_f, ff.app.config['DATABASE'] = tempfile.mkstemp()
        ff.app.testing = True
        self.app = ff.app.test_client()
        self.db = init_db(ff.app.config['DATABASE'])

    def tearDown(self):
        self.db.close()
        os.close(self.db_f)
        os.unlink(ff.app.config['DATABASE'])

    def test_login_form(self):
        """Should return 'login_form'"""
        rv = self.app.post('/', data=dict(
            username='User',
            password='UserPassword'
        ))
        assert b'login_form' in rv.data

    def test_user_info_form(self):
        """Should return 'user_info_form'"""
        rv = self.app.post('/', data=dict(
            username='username',
            user_email='useremail@gmail.com',
            user_phone='+7 988 988 88 88',
            birthday='01.01.1980'
        ))
        assert b'user_info_form' in rv.data

    def test_send_email_form(self):
        """Should return 'send_email_form'"""
        rv = self.app.post('/', data=dict(
            recipient='username',
            rec_email='some@mail.ru',
            message='This is a message'
        ))
        assert b'send_email_form' in rv.data

    def test_form_with_not_existing_field_name(self):
        """Should return {'field':'type'} doc"""
        data = {'user': 'Ivan', 'password': '12345'}
        rv = self.app.post('/', data=data)
        assert b'{"user": "text", "password": "text"}' in rv.data

    def test_form_with_extra_fields(self):
        """Should return form name even if form contains extra fields"""
        data = {'recipient': 'Vlad', 'rec_email': 'mymail@mail.ru'}
        rv = self.app.post('/', data=data)
        assert b'send_email_form' in rv.data

    def test_form_with_lack_of_fields(self):
        """Should return {'field':'type'} doc"""
        data = {'username': 'batman', 'password': 'qwerty1', 'new_password': 'qwerty2'}
        rv = self.app.post('/', data=data)
        assert b'{"username": "text", "password": "text", "new_password": "text"}' in rv.data

    def test_type_validation(self):
        """Should return {'field':'type'} doc"""
        data = {'date': '01.12.1980', 'email': 'some@mail.ru', 'phone': '+7 938 555 55 55', 'text': 'Some text here...'}
        rv = self.app.post('/', data=data)
        assert b'{"date": "date", "email": "email", "phone": "phone", "text": "text"}' in rv.data

    def test_type_validation_with_incorrect_inputs(self):
        """Should return {'field':'text'} doc"""
        data = {'date': '32.15.1980', 'email': 'in@some@mail.ru', 'phone': '+37 938 555 55 55', 'text': 'Some text'}
        rv = self.app.post('/', data=data)
        assert b'{"date": "text", "email": "text", "phone": "text", "text": "text"}' in rv.data


if __name__ == '__main__':
    unittest.main()
