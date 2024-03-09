import os

import psycopg2
from dotenv import load_dotenv


class Employers:
    """
    Заполняет таблицу "employers" в базе данных "job_search" данными о работодателях.
    """
    load_dotenv()
    password_db: str | None = os.getenv("PASS_DB_PGSQL")

    def __init__(self, emp_dict: dict, password: str | None = password_db):
        self.emp_dict = emp_dict
        self.conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")

    def add_emp_to_db(self) -> None:
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        f"INSERT INTO employers VALUES (%s, %s, %s)",
                        (
                            self.emp_dict["employer_id"],
                            self.emp_dict["employer_name"],
                            self.emp_dict["open_vacancies"],
                        ),
                    )
        finally:
            self.conn.close()


class Vacancies:
    """
    Заполняет таблицу "vacancies" в базе данных "job_search" данными о вакансиях.
    """
    load_dotenv()
    password_db: str | None = os.getenv("PASS_DB_PGSQL")

    def __init__(self, vac_dict: dict, password: str | None = password_db):
        self.vac_dict = vac_dict
        self.conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")

    def add_vac_to_db(self) -> None:
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        f"INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                        (
                            self.vac_dict["vacancy_id"],
                            self.vac_dict["vacancy_name"],
                            self.vac_dict["employer_id"],
                            self.vac_dict["salary"],
                            self.vac_dict["vacancy_url"],
                        ),
                    )
        finally:
            self.conn.close()
