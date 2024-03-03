from pprint import pprint

import requests


class HeadHunterAPI:
    """
    Получение данных о работодателях и вакансиях этого работодателя
    """

    def __init__(self, employer_id: int):
        self.employer_id = employer_id
        self.__basic_url = f"https://api.hh.ru/employers/{self.employer_id}"

    def get_emp_info_from_api(self):
        """
        Получение данных о работодателе
        :return: Данные о работодателе
        """

        response = requests.get(self.__basic_url)
        emp_json = response.json()
        emp_dict = dict(employer_id=int(emp_json["id"]), employer_name=emp_json["name"],
                        open_vacancies=emp_json["open_vacancies"])

        return emp_dict

    def get_vac_info_from_api(self):
        """
        Получение данных о вакансиях определенного работодателя
        :return: Данные о вакансиях
        """

        vac_list = []

        params = {"employer_id": self.employer_id}
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        vac_json = response.json()
        for vacancy in vac_json["items"]:
            vac_dict = dict(vacancy_id=int(vacancy["id"]), vacancy_name=vacancy["name"],
                            salary=get_salary(vacancy),
                            vacancy_url=vacancy["alternate_url"])
            vac_list.append(vac_dict)

        return vac_list


def get_salary(vacancy: dict) -> int | None:
    """
    Принимает на вход словарь с описанием вакансии и возвращает зарплату.
    Если указана зарплата "От" - возвращает её, если указана ТОЛЬКО зарплата "До" - возвращает её.
    Во всех остальных случаях возвращает None.
    :param vacancy: Словарь с описанием вакансии
    :return: Зарплата (опционально None, если не указана).
    """
    if vacancy["salary"] is None:
        return None
    elif "from" in vacancy["salary"] and vacancy["salary"]["from"] is not None:
        return vacancy["salary"]["from"]
    elif "to" in vacancy["salary"] and vacancy["salary"]["to"] is not None:
        return vacancy["salary"]["to"]
    else:
        return vacancy["salary"]


if __name__ == '__main__':
    hh = HeadHunterAPI(1455)
    pprint(hh.get_emp_info_from_api())
    pprint(hh.get_vac_info_from_api())