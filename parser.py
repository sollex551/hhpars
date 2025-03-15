import json
import requests
import random
import os


def load_existing_vacancies():
    if os.path.exists("vacancy_info.json"):
        with open("vacancy_info.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def find_vacancy_ids():
    url = "https://api.hh.ru/vacancies"
    page = random.randint(1, 5)  
    params = {"text": "python", "area": "97", "per_page": "5", "page": page}
    response = requests.get(url, params=params)
    data = response.json()

    vacancies = [item.get("id") for item in data.get("items", [])]
    return vacancies

def return_description_by_id():
    existing_vacancies = load_existing_vacancies()  
    print(existing_vacancies)
    existing_ids = {vacancy["Ссылка"].split("/")[-1] for vacancy in existing_vacancies}  

    new_vacancies = []
    for vacancy_id in find_vacancy_ids():
        if vacancy_id in existing_ids:
            print(f"Вакансия {vacancy_id} уже есть в базе")
            continue  

        url = f"https://api.hh.ru/vacancies/{vacancy_id}?host=hh.ru"
        response = requests.get(url)
        vacancy = response.json()

        print(f'Вакансия "{vacancy["name"]}" Загружена')

        salary_info = vacancy.get("salary")
        if salary_info:
            salary_text = f'{salary_info.get("from", "Не указано")} - {salary_info.get("to", "Не указано")} {salary_info.get("currency", "")}'
        else:
            salary_text = "Не указано"

        info = {
            "Вакансия": vacancy["name"],
            "Компания": vacancy["employer"]["name"],
            "Город": vacancy["area"]["name"],
            "Зарплата": salary_text,
            "Короткое описание": vacancy.get("snippet", {}).get("requirement", "Нет краткого описания"),
            "Описание": vacancy.get("description", "Нет описания").replace("<p>", "").replace("</p>", "\n").replace(
                "<br />", "\n"),
            "Ссылка": vacancy["alternate_url"]
        }
        new_vacancies.append(info)

    if new_vacancies:
        with open("vacancy_info.json", "w", encoding="utf-8") as file:
            json.dump(existing_vacancies + new_vacancies, file, ensure_ascii=False, indent=4)
        print("Новые вакансии добавлены в файл.")
    else:
        print("Нет новых вакансий для добавления.")


