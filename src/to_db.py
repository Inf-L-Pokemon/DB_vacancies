from dotenv import load_dotenv

import os
import psycopg2


class EmployersToDB:

    load_dotenv()
    password_db: str | None = os.getenv("PASS_DB_PGSQL")

    def __init__(self, emp_dict: dict, password_db=password_db):
        self.emp_dict = emp_dict
        self.conn = psycopg2.connect(host="localhost", user="postgres", password=password_db)

    def create_db_emp(self):
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute('CREATE DATABASE employers (employer_id PRIMARY KEY int, employer_name varchar(100), '
                                'open_vacancies int)')
        finally:
            self.conn.close()

    def add_emp_to_db(self):
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(f'INSERT INTO employers VALUES ({self.emp_dict["employer_id"]}, '
                                '{self.emp_dict["employer_name"]}, {self.emp_dict["open_vacancies"]})')
        finally:
            self.conn.close()

    def del_db_emp(self):
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute('DROP DATABASE employers')
        finally:
            self.conn.close()
