import os
from datetime import date

from flask import Blueprint, render_template, current_app, url_for

from database.operations import select
from database.sql_provider import SQLProvider

from auth_routes import check_access
from report_routes import get_reports
from Redis.cache import fetch_from_cache, update_from_cache

query_app = Blueprint('query_app', __name__, template_folder='templates', static_folder='static')

sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def get_info(file_name):
    sql = sql_provider.get_sql(f'{file_name}.sql', {})
    result, _ = select(current_app.config['db_config'], sql)
    print(result)
    return result


def curr_date():
    d = date.today().strftime('%d/%m/%Y')
    return d


@query_app.route('/all_products', methods=['GET', 'POST'])
def all_products():
    cache_config = current_app.config['cache_config']
    cache_select = update_from_cache('product_info', cache_config)(select)
    sql = sql_provider.get_sql('all_products.sql', {})
    result, schema = cache_select(current_app.config['db_config'], sql)
    print(result, schema)
    return render_template('db_result.html',
                           schema=schema,
                           result=result,
                           title='Номенклатура товаров',
                           add_link=url_for('add_app.new_product'),
                           **check_access(),
                           reports=get_reports())


@query_app.route('/all_groups', methods=['GET', 'POST'])
def all_groups():
    cache_config = current_app.config['cache_config']
    cache_select = update_from_cache('group_info', cache_config)(select)
    sql = sql_provider.get_sql('all_group.sql', {})
    result, schema = cache_select(current_app.config['db_config'], sql)
    return render_template('db_result.html',
                           schema=schema,
                           result=result,
                           title='Группы товаров',
                           add_link=url_for('add_app.new_group'),
                           **check_access(), reports=get_reports())


@query_app.route('/all_resources', methods=['GET', 'POST'])
def all_resources():
    sql = sql_provider.get_sql('all_resources.sql', {})
    result, schema = select(current_app.config['db_config'], sql)
    access = check_access()
    access['add_display'] = 'none'
    return render_template('db_result.html', schema=schema, result=result,
                           title='Текущие остатки на складе',
                           **access, reports=get_reports())


@query_app.route('/all_invoices', methods=['GET', 'POST'])
def all_invoices():
    sql = sql_provider.get_sql('all_invoices.sql', {})
    result, schema = select(current_app.config['db_config'], sql)
    print("HEY", schema, " ", result)
    return render_template('all_invoices.html', schema=schema, result=result,
                           title='Накладные',
                           add_link=url_for('add_app.new_invoice'),
                           **check_access(), reports=get_reports())


@query_app.route("/invoice_list/<invoice_num>", methods=['GET', 'POST'])
def invoice_list(invoice_num):
    sql = sql_provider.get_sql('specific_invoice.sql', {'invoice': invoice_num})
    invoice, _ = select(current_app.config['db_config'], sql)
    invoice = invoice[0]

    sql = sql_provider.get_sql('invoice_list.sql', {'invoice': invoice['Номер накладной']})
    result, schema = select(current_app.config['db_config'], sql)
    print(result)
    return render_template('db_result.html', schema=schema, result=result,
                           title=f"Накладная №\t{invoice['Номер накладной']} от {invoice['Дата']}",
                           supplier=f"Поставщик:\t{invoice['Поставщик']}",
                           **check_access(), flag='none', reports=get_reports(), add_display='none')


@query_app.route('/all_suppliers', methods=['GET', 'POST'])
def all_suppliers():
    sql = sql_provider.get_sql('all_suppliers.sql', {})
    result, schema = select(current_app.config['db_config'], sql)
    access = check_access()
    if access['user'] == 'Начальник склада':
        access['add_display'] = 'none'
    elif access['user'] == 'Менеджер по закупкам':
        access['add_display'] = ''
    return render_template('db_result.html', schema=schema, result=result,
                           title='Поставщики',
                           add_link=url_for('add_app.new_supplier'),
                           **access, reports=get_reports())
