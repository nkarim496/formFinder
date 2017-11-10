from flask import Flask, request, make_response
from tinydb import TinyDB, Query
import os
import re
import json


app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.json')
))
db = TinyDB(app.config['DATABASE'])


def get_type(value):
    """проводит валидацию value и возвращает
    один тип (date, phone, email, text)"""
    date = re.compile('''(^(19|20)\d\d               # год 1900-2099
                         [- /.]                      # разделитель
                         (0[1-9]|1[012])             # месяц 01-12
                         [- /.]                      # разделитель
                         (0[1-9]|[12][0-9]|3[01])$)  # день 01-31
                         |                           # или
                         (^(0[1-9]|[12][0-9]|3[01])  # день 01-31
                         [- /.]                      # разделитель
                         (0[1-9]|1[012])             # месяц 01-12
                         [- /.]                      # разделитель
                         (19|20)\d\d$)               # год 1900-2099
                      ''', re.VERBOSE)

    email = re.compile('''(^[a-zA-Z0-9_.+-]+         # почта
                          @                          # разделитель
                          [a-zA-Z0-9-]+              # mail, yandex и т.п.
                          \.                         # точка
                          [a-zA-Z0-9-.]+$)           # ru, com и т.п.
                       ''', re.VERBOSE)
    phone = re.compile('''^((8|\+7)[\- ]?)?          # код страны +7 или 8, либо отсутствует
                          (\(?\d{3}\)?)              # код оператора в скобках, либо без
                          [\- ]?                     # разделитель
                          \d{3}                      # 3 цифры
                          [\- ]?                     # разделитель
                          \d{2}                      # 2 цифры
                          [\- ]?                     # разделитель
                          \d{2}$                     # 2 цифры
                       ''', re.VERBOSE)
    if date.match(value):
        return 'date'
    elif phone.match(value):
        return 'phone'
    elif email.match(value):
        return 'email'
    return 'text'


def has_fields(form_fields, request_fields):
    """возвращает True если все поля request_fields
    имеются в форме"""
    ff = [(f['name'], f['type']) for f in form_fields]
    return all((field[0], field[1]) in ff for field in request_fields)


@app.route('/', methods=['POST'])
def index():
    # баг в Query.test нельзя передать list,
    # приходится передавать tuple
    # https://forum.m-siemens.de/d/4-error-with-any-and-all-queries
    fields = tuple((name, get_type(value)) for name, value in request.form.items())
    forms = db.search(Query().fields.test(has_fields, fields))
    resp = make_response(" ".join([form['name'] for form in forms]) if forms else json.dumps({field[0]: field[1] for field in fields}))
    print(resp.data)
    return resp

if __name__ == '__main__':
    app.run()
