import os
from pymysql.err import IntegrityError
from flask import Blueprint, request, render_template, current_app, redirect, url_for

from database.operations import select, insert
from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from query_routes import get_info, curr_date
from datetime import date
from auth_routes import check_access
from report_routes import get_reports

add_app = Blueprint('add_app', __name__, template_folder='templates', static_folder='static')

sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@add_app.route('/new_invoice', methods=['GET', 'POST'])
def new_invoice():
    invoice_num = int(get_info('last_invoice')[0]['in_id']) + 1
    if request.method == 'GET':
        products = get_info('products_info')
        suppliers = get_info('suppliers_info')
        print(products)
        return render_template('new_invoice.html',
                               suppliers=suppliers,
                               products=products,
                               curr_date=curr_date(),
                               invoice_num=invoice_num,
                               **check_access(), reports=get_reports())
    else:
        supplier = request.form.get('supplier')
        p_id = request.form.getlist('product')
        amount = request.form.getlist('amount')
        price = request.form.getlist('price')
        with DBContextManager(current_app.config['db_config']) as cursor:
            if cursor:
                input = {'date': str(date.today()), 'supplier': supplier}
                sql = sql_provider.get_sql('new_invoice.sql', input)
                cursor.execute(sql)
                for i in range(len(p_id)):
                    input = {'product': p_id[i], 'amount': amount[i], 'price': price[i], 'invoice': invoice_num}
                    sql = sql_provider.get_sql('new_invoice_list.sql', input)
                    cursor.execute(sql)
                    return redirect(url_for('query_app.all_invoices'))


@add_app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    groups = get_info('all_group')
    if request.method == 'GET':
        return render_template('insert_into_product.html',
                               title='Номенклатура товара: новая запись',
                               groups=groups,
                               **check_access(), err_dis='none', reports=get_reports())
    else:
        p_name = request.form.get('p_name')
        m_unit = request.form.get('m_unit')
        group = request.form.get('group')
        input = {'p_name': p_name, 'm_unit': m_unit, 'group': group}
        sql = sql_provider.get_sql('new_product.sql', input)
        code = insert(current_app.config['db_config'], sql)
        if code == - 1:
            return render_template('insert_into_product.html',
                                   title='Номенклатура товара: новая запись',
                                   groups=groups,
                                   **check_access(), error='Ошибка! Введенные данные уже существуют',
                                   reports=get_reports())
        return redirect(url_for('query_app.all_products'))


@add_app.route('/new_group', methods=['GET', 'POST'])
def new_group():
    if request.method == 'GET':
        return render_template('insert_into_group.html',
                               title='Группа товаров: новая запись',
                               **check_access(), err_dis='none',
                               reports=get_reports())
    else:
        g_name = request.form.get('g_name')
        input = {'group': g_name}
        sql = sql_provider.get_sql('new_group.sql', input)

        code = insert(current_app.config['db_config'], sql)
        if code == -1:
            return render_template('insert_into_group.html',
                                   title='Группа товаров: новая запись',
                                   **check_access(), error='Ошибка! Введенные данные уже существуют',
                                   reports=get_reports())

        return redirect(url_for('query_app.all_groups'))


@add_app.route('/new_supplier', methods=['GET', 'POST'])
def new_supplier():
    if request.method == 'GET':
        return render_template('insert_into_supplier.html',
                               title='Поставщики: новая запись',
                               **check_access(), err_dis='none', reports=get_reports())
    else:
        s_name = request.form.get('s_name')
        phone_number = request.form.get('phone_number')
        city = request.form.get('city')
        bank_name = request.form.get('bank_name')
        bank_acc = request.form.get('bank_acc')
        contract_date = request.form.get('contract_date')
        term_time = request.form.get('term_time')
        input = {'s_name': s_name, 'phone_number': phone_number,
                 'city': city, 'bank_name': bank_name,
                 'bank_acc': bank_acc, 'contract_date': contract_date,
                 'term_time': term_time}

        sql = sql_provider.get_sql('new_supplier.sql', input)
        code = insert(current_app.config['db_config'], sql)
        if code == -1:
            return render_template('insert_into_supplier.html',
                                   title='Поставщики: новая запись',
                                   **check_access(), error='Ошибка! Введенные данные уже существуют',
                                   reports=get_reports())
        return redirect(url_for('query_app.all_suppliers'))
