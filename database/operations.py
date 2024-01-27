from typing import Tuple, List, Dict, Any
from database.connection import DBContextManager
from pymysql.err import IntegrityError


def select(db_config: dict, sql: str) -> tuple[list[dict[Any, Any]], list[Any]]:
    result = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            print(cursor)
            return ValueError('Cursor not found'), None
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = [dict(zip(schema, row)) for row in cursor.fetchall()]
    return result, schema


def insert(db_config: dict, sql: str):
    code = 0
    with DBContextManager(db_config) as cursor:
        try:
            cursor.execute(sql)
        except IntegrityError as err:
            print("Error in Insert", err.args[0])
            code = -1
    return code


def call_procedure(db_config: dict, sql: str):
    code = 0
    with DBContextManager(db_config) as cursor:
        try:
            cursor.execute(sql)
        except IntegrityError as err:
            print("Error in Procedure", err.args[0])
            code = -1
        except ValueError as err:
            print("Error in Procedure", err.args[0])
            code = -2
    return code
