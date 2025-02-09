from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests

def get_vacancies_data():
    # Попытка получить данные из кэша
    data = cache.get('vacancies_data')

    if not data:
        # Если данных нет в кэше, запросим их из базы данных
        data = Vacancy.objects.all()  # Пример запроса к базе данных
        # Закэшируем данные на 10 минут
        cache.set('vacancies_data', data, timeout=600)  # timeout в секундах

    return data

# Create your views here.
def hello(request):
    template = loader.get_template('base.html')
    context = {
        'title': 'Администратор баз данных — ключевая роль в мире IT',
        'content': '''<p>Администратор баз данных (DBA, Database Administrator) — это специалист, отвечающий за проектирование, настройку, поддержку и безопасность баз данных. В современном мире, где данные являются одним из самых ценных ресурсов, роль администратора баз данных становится критически важной для успешной работы любой компании.</p>

                     <p>Администратор баз данных обеспечивает бесперебойную работу систем хранения и обработки информации, следит за производительностью баз данных, оптимизирует запросы и обеспечивает защиту данных от несанкционированного доступа. В его обязанности входит резервное копирование данных, восстановление информации в случае сбоев, а также мониторинг и устранение неполадок.</p>

                     <p>Профессия требует глубоких знаний в области IT, понимания принципов работы СУБД (систем управления базами данных), таких как MySQL, PostgreSQL, Oracle, Microsoft SQL Server и других. Администратор баз данных должен разбираться в языках запросов (например, SQL), понимать архитектуру баз данных и уметь работать с большими объемами информации.</p>

                     <p>Кроме технических навыков, администратор баз данных должен обладать аналитическим мышлением, внимательностью и способностью быстро принимать решения в критических ситуациях. Эта профессия подходит для тех, кто любит работать с данными, решать сложные задачи и постоянно развиваться в сфере IT.</p>

                     <p>Администраторы баз данных востребованы в самых разных отраслях: от финансов и медицины до e-commerce и государственных структур. Они играют ключевую роль в обеспечении стабильности и безопасности информационных систем, что делает их незаменимыми специалистами в любой компании.</p>

                     <p>Если вы хотите стать частью мира IT, работать с передовыми технологиями и влиять на успех бизнеса, профессия администратора баз данных — это отличный выбор.</p>'''
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
     context = {
         'title': 'Навыки',
     }
     return HttpResponse(template.render(context))

def vacancies(request):
    # Шаблон для рендеринга
    template = loader.get_template('vacancies.html')

    # Выполняем GET-запрос к API HH
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "администратор баз данных",  # Ключевые слова для поиска вакансий
        "per_page": 10,  # Количество вакансий на странице
    }
    response = requests.get(url, params=params)

    # Проверяем успешность запроса
    '''
    if response.status_code == 200:
        vacancies_data = response.json()  # Получаем JSON-ответ
        vacancies_text = "Вакансии:\n\n"
        for vacancy in vacancies_data.get('items', []):
            vacancies_text += f"Название: {vacancy.get('name', 'Нет данных')}\n"
            vacancies_text += f"Компания: {vacancy.get('employer', {}).get('name', 'Нет данных')}\n"
            vacancies_text += f"Зарплата: {vacancy.get('salary', 'Нет данных')}\n"
            vacancies_text += f"Регион: {vacancy.get('area', {}).get('name', 'Нет данных')}\n"
            vacancies_text += f"Дата публикации: {vacancy.get('published_at', 'Нет данных')}\n"
            vacancies_text += "\n"
    else:
        vacancies_text = "Ошибка при получении данных с API HH."
    '''
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


    # Контекст для передачи в шаблон
    context = {
        'title': 'Вакансии',
        'vacancies': vacancies_list,  # Передаем массив вакансий в шаблон
    }

    # Рендерим шаблон и возвращаем ответ
    return HttpResponse(template.render(context, request))