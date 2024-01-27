import os

from flask import Blueprint, render_template, current_app, json
from flask import request, redirect, url_for

from database.operations import select
from database.sql_provider import SQLProvider

from report.report_routes import dump_reports
auth_app = Blueprint('auth_app', __name__, template_folder='templates', static_folder='static')

sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))



def user_info():
    with open('config/user.json', 'r') as outfile:
        user = json.load(outfile)
    return user


def get_group(login: str, password: str):
    if (('\'' in login) or ('`' in login)) and (('\'' in password) or ('`' in password)):
        return False
    input = {'login': login, 'password': password}
    sql = sql_provider.get_sql('get_group.sql', input)
    group, _ = select(current_app.config['db_config'], sql)
    print(group)
    try:
        return group[0]['group']
    except IndexError:
        return False
    except TypeError:
        return 'DB_Error'
    except UnboundLocalError:
        return False


def check_access():
    group = user_info()['group']
    if group == 'admin':
        return {'user': 'Администратор'}
    else:
        with open('config/access.json', 'r') as outfile:
            access = json.load(outfile)
        print(access)
        return access[group]


@auth_app.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html', err_dis='none')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        group = get_group(login, password)
        print(login, " ", password, " ", group)
        if group is False:
            return render_template('auth.html',
                                   error='Неправильный логин или пароль!')
        elif group == "DB_Error":
            return render_template('auth.html',
                                   error="Невозможно подключиться к Базе данных. Обратитесь к "
                                         "Администратору!")
        if login and password:
            input = {'login': login, 'password': password}
            sql = sql_provider.get_sql('check_user.sql', input)
            result = select(current_app.config['db_config'], sql)
            print(result[0])
            input['group'] = group
            with open("config/user.json", "w") as outfile:
                json.dump(input, outfile)
            dump_reports()
            return redirect(url_for('main_menu'))
