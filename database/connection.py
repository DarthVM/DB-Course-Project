from typing import Optional
from pymysql import connect
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from pymysql.err import OperationalError, IntegrityError
import pymysql.err


class DBContextManager:
    def __init__(self, config: dict):
        self.config = config
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

    def __enter__(self) -> Optional[pymysql.cursors.Cursor]:
        try:
            self.conn = connect(**self.config)
            print(self.conn)
            self.cursor = self.conn.cursor()
            print(self.cursor)
            return self.cursor
        except OperationalError as err:

            if err.args[0] == 1062:
                return None
            elif err.args[0] == 1049:
                return None
            elif err.args[0] == 2003:
                return None
            else:
                print(err.args)
                print('not ok')
                return None
        except pymysql.err.IntegrityError as err:
            print('no')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type)
            print(exc_val)
            print(exc_val.args[0])
        if self.conn and self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True
