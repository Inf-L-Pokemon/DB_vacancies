import os

from dotenv import load_dotenv

from src.create_del_table import (
    create_table_employers,
    create_table_vacancies,
    del_table_employers,
    del_table_vacancies,
)
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

    while welcome_answer != ["1", "2", "3"]:
        if welcome_answer == "3":
            quit("До встречи!")
        elif welcome_answer == "1" or welcome_answer == "2":
            break
        else:
            welcome_answer = input()
            continue

    try:
        create_table_employers(password_db)
        create_table_vacancies(password_db)
    except Exception as ex:
        print("Упс... Что-то пошло не так. Проверьте ещё раз необходимые параметры для базы данных 'job_search'.")
        quit(ex.__repr__())

    try:
        for emp_id in employers_id.values():
            response = HeadHunterAPI(emp_id)

            emp_to_db = Employers(response.get_emp_info_from_api())
            emp_to_db.add_emp_to_db()

            for vac in response.get_vac_info_from_api():
                Vacancies(vac).add_vac_to_db()
    except Exception as ex:
        print("Произошла непредвиденная ошибка. Пожалуйста, попробуйте повторить данную процедуру позже.")
        quit(ex.__repr__())


if __name__ == "__main__":
    del_table_vacancies(password_db)
    del_table_employers(password_db)
    main()
