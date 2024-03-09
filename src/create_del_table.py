import psycopg2


def create_table_employers(password: str) -> None:
    """
    Создает таблицу с названием "employers" в базе данных "job_search"
    :param password: Пароль для соединения с базой данных
    :return: None
    """
    conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS employers (employer_id int PRIMARY KEY, employer_name varchar(100), "
                    "open_vacancies int)"
                )
    finally:
        conn.close()


def create_table_vacancies(password: str) -> None:
    """
    Создает таблицу с названием "vacancies" в базе данных "job_search"
    :param password: Пароль для соединения с базой данных
    :return: None
    """
    conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS vacancies (vacancy_id int PRIMARY KEY, vacancy_name varchar(100), "
                    "employer_id int REFERENCES employers(employer_id) NOT NULL, "
                    "salary int, vacancy_url varchar(100))"
                )
    finally:
        conn.close()


def del_table_employers(password: str) -> None:
    """
    Удаляет таблицу с названием "employers" из базы данных "job_search"
    :param password: Пароль для соединения с базой данных
    :return: None
    """
    conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS employers CASCADE")
    finally:
        conn.close()


def del_table_vacancies(password: str) -> None:
    """
    Удаляет таблицу с названием "vacancies" из базы данных "job_search"
    :param password: Пароль для соединения с базой данных
    :return: None
    """
    conn = psycopg2.connect(host="localhost", user="postgres", password=password, database="job_search")
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS vacancies CASCADE")
    finally:
        conn.close()
