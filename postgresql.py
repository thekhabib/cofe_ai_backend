import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

class Database:
    def __init__(self, dbname="qr-library", user="postgres", password="123qwe", host="localhost", port="5432"):
        self.db_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }

    @property
    def connection(self):
        return psycopg2.connect(**self.db_params)

    def execute(self, sql_query: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        
        connection = self.connection
        connection.autocommit = False
        cursor = connection.cursor(cursor_factory=DictCursor)
        data = None
        
        try:
            cursor.execute(sql_query, parameters)
            
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
                
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
            
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            full_name TEXT,
            telegram_id BIGINT UNIQUE
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql_query, parameters: dict):
        if not parameters:
            return sql_query, ()
            
        conditions = []
        values = []
        for key, value in parameters.items():
            conditions.append(f"{key} = %s")
            values.append(value)
            
        sql_query = sql_query.replace("WHERE;", "WHERE " + " AND ".join(conditions) + ";")
        return sql_query, tuple(values)

    def add_user(self, telegram_id: int, full_name: str):
        sql = """
        INSERT INTO users (telegram_id, full_name) 
        VALUES (%s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
        """
        self.execute(sql, parameters=(telegram_id, full_name), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users;
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE;"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM users;", commit=True)
    
    def all_users_id(self):
        return self.execute("SELECT telegram_id FROM users;", fetchall=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")