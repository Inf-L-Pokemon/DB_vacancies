import os
from pprint import pprint

import psycopg2
from dotenv import load_dotenv


class DBManager:
    """
    Класс работы с базой данных.
    """
    load_dotenv()
    password_db: str | None = os.getenv("PASS_DB_PGSQL")

    def __init__(self, password: str | None = password_db):
        self.conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")

    def connect_to_db(self, sql_code: str, quantity: int) -> None:
        """
        Соединение с базой данных.
        :param quantity: Количество строк при выводе данных
        :param sql_code: Код, который непосредственно будет выполняться в базе данных.
        :return: None
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(sql_code)
                    pprint(cur.fetchmany(quantity))
        except Exception as ex:
            print("Упс! Наверное, что-то случилось... Мы обязательно разберёмся и накажем виновных!")
            print(ex.__repr__())
        finally:
            self.conn.close()

    def get_companies_and_vacancies_count(self, quantity: int) -> None:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: None
        """
        self.connect_to_db("SELECT employer_name, open_vacancies FROM employers", quantity)

    def get_all_vacancies(self, quantity: int) -> None:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return: None
        """
        self.connect_to_db(
            "SELECT employers.employer_name, vacancy_name, salary, vacancy_url FROM vacancies JOIN employers USING "
            "(employer_id) WHERE salary IS NOT NULL",
            quantity
        )

    def get_avg_salary(self, quantity: int = 1) -> None:
        """
        Получает среднюю зарплату по вакансиям.
        :return: None
        """
        self.connect_to_db("SELECT AVG(salary) FROM vacancies", quantity)

    def get_vacancies_with_higher_salary(self, quantity: int) -> None:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: None
        """
        self.connect_to_db(
            "SELECT employer_name, vacancy_name, salary, vacancy_url FROM vacancies "
            "JOIN employers USING (employer_id) WHERE salary > (SELECT AVG(salary) FROM vacancies)",
            quantity
        )

    def get_vacancies_with_keyword(self, search_word: str, quantity: int) -> None:
        """
        Получает список всех вакансий, в названии которых содержится переданное в метод слово.
        :param quantity: Количество строк при выводе данных
        :param search_word: Слово для поиска в названии вакансии.
        :return: None
        """
        self.connect_to_db(
            "SELECT employer_name, vacancy_name, salary, vacancy_url FROM vacancies "
            f"JOIN employers USING (employer_id) WHERE vacancy_name LIKE '%{search_word.lower()}%' "
            f"OR vacancy_name LIKE '%{search_word.capitalize()}%'",
            quantity
        )
