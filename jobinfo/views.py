from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from django.core.cache import cache

def get_vacancies_data():

    # Выполняем GET-запрос к API HH
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "администратор баз данных",  # Ключевые слова для поиска вакансий
        "only_with_salary": "true",
        "per_page": 10,  # Количество вакансий на странице
    }
    response = requests.get(url, params=params)

    # Массив для хранения данных о вакансиях
    vacancies_list = []

    # Проверяем успешность запроса
    if response.status_code == 200:
        vacancies_data = response.json()  # Получаем JSON-ответ
        for vacancy in vacancies_data.get('items', []):
            # Формируем словарь с данными о вакансии
            vacancy_info = {
                'name': vacancy.get('name', 'Нет данных'),
                'employer': vacancy.get('employer', {}).get('name', 'Нет данных'),
                'salary': vacancy.get('salary', 'Нет данных'),
                'area': vacancy.get('area', {}).get('name', 'Нет данных'),
                'published_at': vacancy.get('published_at', 'Нет данных'),
            }
            vacancies_list.append(vacancy_info)  # Добавляем вакансию в массив
    else:
        vacancies_list = []  # Если запрос не удался, массив остается пустым

    return vacancies_list

# Create your views here.
def hello(request):
    template = loader.get_template('home.html')
    context = {
        'title': 'Администратор баз данных — ключевая роль в мире IT',
    }
    return HttpResponse(template.render(context))

def stat(request):
    template = loader.get_template('stat.html')
    context = {
        'title': 'Статистика',
    }
    return HttpResponse(template.render(context))

def demand(request):
    template = loader.get_template('base.html')
    context = {
        'title': 'Востребованность',
    }
    return HttpResponse(template.render(context))

def geo(request):
    template = loader.get_template('base.html')
    context = {
        'title': 'География',
    }
    return HttpResponse(template.render(context))

def skills(request):
     template = loader.get_template('skills.html')

     vacancies_list = get_vacancies_data()

     context = {
         'title': 'Навыки',
     }
     return HttpResponse(template.render(context, request))

def vacancies(request):
    # Шаблон для рендеринга
    template = loader.get_template('vacancies.html')

    # Проверяем успешность запроса

    vacancies_list = get_vacancies_data()

    # Контекст для передачи в шаблон
    context = {
        'title': 'Вакансии',
        'vacancies': vacancies_list,  # Передаем массив вакансий в шаблон
    }

    # Рендерим шаблон и возвращаем ответ
    return HttpResponse(template.render(context, request))