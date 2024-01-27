from flask import Blueprint, request, render_template, current_app, json
from database.operations import select, call_procedure
from database.sql_provider import SQLProvider
import os
from datetime import datetime, timedelta

report_app = Blueprint('report_app', __name__, template_folder='templates', static_folder='static')

sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def get_name(rep_type):
    with open('config/rep_name.json', 'r') as outfile:
        rep_name = json.load(outfile)
    return rep_name[rep_type]


def month_rus(month=None):
    m_ru = {
        'January': 'Январь',
        'February': 'Февраль',
        'March': 'Март',
        'April': 'Апрель',
        'May': 'Май',
        'June': 'Июнь',
        'July': 'Июль',
        'August': 'Август',
        'September': 'Сентябрь',
        'October': 'Октябрь',
        'November': 'Ноябрь',
        'December': 'Декабрь'
    }
    if month:
        return m_ru[month]
    else:
        return m_ru

def form_name(type, month, year):
    return str(get_name(type)) + f" ({month_rus(month)}, {year})"

def get_reports():
    with open('blueprints/report/config/reports_exist.txt', 'r') as file:
        data = file.readlines()
    print(data)
    return data


def get_dates(month, year):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month+1, 1) - timedelta(days=1)
    return start_date, end_date



def dump_reports():
    sql = sql_provider.get_sql('all_reports.sql', {})
    data, _ = select(current_app.config['db_config'], sql)
    with open('blueprints/report/config/reports_exist.txt', 'w') as file:
        for report in data:
            name = form_name(report['report_type'], report['month'], report['year'])
            file.write(name)
            file.write('\n')


def check_report(name: str):
    with open('blueprints/report/config/reports_exist.txt', 'r') as file:
        data = file.readlines()
    if name in data:
        return True
    return False



@report_app.route('/new_report', methods=['GET', 'POST'])
def new_report():
    if request.method == 'GET':
        return render_template('new_report.html',
                               title='Отчет: новая запись',
                               reports=get_reports())
    else:
        rep_type = request.form.get('rep_type')
        month = request.form.get('month')
        year = request.form.get('year')
        name = form_name(rep_type, month, year)


        if check_report(name):
            return render_template('new_report.html',
                                   title='Отчет: новая запись',
                                   reports=get_reports(),
                                   error='Такой отчет уже существует!')
        start_date, end_date = get_dates(month, year)
        input = {'rep_type': rep_type, 'start_date': start_date, 'end_date': end_date}
        sql = sql_provider.get_sql('new_report.sql', input)
        code = call_procedure(current_app.config['db_config'], sql)
        dump_reports()
        sql = sql_provider.get_sql('las_report.sql')
        result, schema = select(current_app.config['db_config'], sql)
        return render_template('report_result.html', schema=schema, result=result,
                               reports=get_reports())






@report_app.route('/report/<rep_id>', methods=['GET', 'POST'])
def report_list(rep_id):
    sql = sql_provider.get_sql('specific_report.sql', {'report': rep_id})
    report, schema = select(current_app.config['db_config'], sql)
    return render_template('report_result.html', result=report, schema=schema)







