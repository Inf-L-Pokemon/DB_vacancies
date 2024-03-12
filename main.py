import os

from dotenv import load_dotenv

from src.db_manager import DBManager
from src.create_del_table import create_table_employers, create_table_vacancies, del_table_employers, \
    del_table_vacancies
from src.to_db import Employers, Vacancies
from src.vac_from_api import HeadHunterAPI

load_dotenv()
password_db: str | None = os.getenv("PASS_DB_PGSQL")

employers_id = {
    "Яндекс": 1740,
    "МТС": 3776,
    "Skyeng": 1122462,
    "Билайн": 4934,
    "Астра": 5060211,
    "Банк ВТБ": 4181,
    "Softline": 2381,
    "Ростелеком Информационные Технологии": 3144945,
    "HeadHunter": 1455,
    "ГК «ХайТэк»": 2262181,
}


def main() -> None:
    print(
        "Доброго времени суток!\nДалее будет создана подборка вакансий (размещенных на сервисе hh.ru) следующих "
        f"компаний:\n{', '.join(employers_id.keys())}."
    )

    welcome_answer = input(
        "\nПроверьте готовность использования программы, указанную в README файле.\n"
        "Введите:\n1 - Всё готово! (PostgreSQL установлен, база данных 'job_search' создана)"
        "\n2 - Не уверен... Давайте попробуем, что будет дальше."
        "\n3 - Что-то мне перехотелось её использовать. Как-нибудь потом.\n"
    )

    while True:
        if welcome_answer == "3":
            quit("До встречи!")
        elif welcome_answer == "1" or welcome_answer == "2":
            break
        else:
            welcome_answer = input()
            continue

    try:
        del_table_vacancies(password_db)
        del_table_employers(password_db)
        create_table_employers(password_db)
        create_table_vacancies(password_db)
    except Exception as ex:
        print("Упс... Что-то пошло не так. Проверьте ещё раз необходимые параметры для базы данных 'job_search'.")
        quit(ex.__repr__())

    try:
        print("\nДанная процедура займёт непродолжительное время. Пожалуйста, наберитесь терпения и подождите...")
        for emp_name, emp_id in employers_id.items():
            response = HeadHunterAPI(emp_id)

            emp_to_db = Employers(response.get_emp_info_from_api())
            emp_to_db.add_emp_to_db()

            vac_to_db = Vacancies(response.get_vac_info_from_api())
            vac_to_db.add_vac_to_db()
            print(f"Добавлены вакансии от {emp_name}")
        print("\nВсё прошло успешно! База данных заполнена вакансиями от указанных выше работодателей.\n")
    except Exception as ex:
        print("Произошла непредвиденная ошибка. Пожалуйста, попробуйте повторить данную процедуру позже.")
        quit(ex.__repr__())

    info_from_db_answer = int(input("Пожалуйста, выберите, какую информацию вы хотите получить по данным вакансиям:\n"
                                    "1 - Список всех компаний и количество вакансий у каждой компании.\n"
                                    "2 - Список всех вакансий с указанием названия компании, названия вакансии и "
                                    "зарплаты и ссылки на вакансию.\n"
                                    "3 - Среднюю зарплату по вакансиям.\n"
                                    "4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                                    "5 - Список всех вакансий, в названии которых содержится переданное вами слово.\n"
                                    "0 - Выход из программы.\n"))

    info_from_db = DBManager()

    while True:
        if info_from_db_answer == 0:
            quit("До встречи!")
        elif info_from_db_answer == 1:
            info_from_db.get_companies_and_vacancies_count(quantity=int(input("Введите количество строк для выдачи:\n")))
            break
        elif info_from_db_answer == 2:
            info_from_db.get_all_vacancies(quantity=int(input("Введите количество строк для выдачи:\n")))
            break
        elif info_from_db_answer == 3:
            info_from_db.get_avg_salary()
            break
        elif info_from_db_answer == 4:
            info_from_db.get_vacancies_with_higher_salary(quantity=int(input("Введите количество строк для выдачи:\n")))
            break
        elif info_from_db_answer == 5:
            search_word = input("Введите слово для поиска:\n")
            info_from_db.get_vacancies_with_keyword(search_word, quantity=int(input("Введите количество строк для "
                                                                                    "выдачи:\n")))
            break
        else:
            info_from_db_answer = int(input())
            continue


if __name__ == "__main__":
    main()
