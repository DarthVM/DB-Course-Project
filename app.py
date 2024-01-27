from flask import render_template, Flask, json, request, redirect, url_for
from auth_routes import auth_app, get_group, user_info, check_access, auth
from query_routes import query_app
from report_routes import report_app, get_reports
from add_routes import add_app

app = Flask(__name__)
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(query_app, url_prefix='/query')
app.register_blueprint(report_app, url_prefix='/report')
app.register_blueprint(add_app, url_prefix='/add')

with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)
app.config['db_config'] = db_config

with open('config/cache_config.json', 'r') as f:
    cache_config = json.load(f)
app.config['cache_config'] = cache_config


@app.route('/main_menu', methods=['GET', 'POST'])
def main_menu():
    return render_template('main_menu.html', **check_access(), reports=get_reports())


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth_app.auth'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
