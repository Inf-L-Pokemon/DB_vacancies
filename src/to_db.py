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

    def __init__(self, vac_list: list, password: str | None = password_db):
        self.vac_list = vac_list
        self.conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")

    def add_vac_to_db(self) -> None:
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    for vac_dict in self.vac_list:
                        cur.execute(
                            f"INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                            (
                                vac_dict["vacancy_id"],
                                vac_dict["vacancy_name"],
                                vac_dict["employer_id"],
                                vac_dict["salary"],
                                vac_dict["vacancy_url"],
                            ),
                        )
        finally:
            self.conn.close()
