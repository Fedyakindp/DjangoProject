from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from jobinfo.models import JobListing
from collections import defaultdict

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

def get_unique_skills_by_year():
    jobs = JobListing.objects.values('published_at', 'key_skills')
    skills_by_year = defaultdict(set)

    for job in jobs:
        year = job['published_at'].year
        skills = job['key_skills'].split(',') if job['key_skills'] else []
        skills_by_year[year].update(skill.strip() for skill in skills)

    sorted_skills = {year: list(skills) for year, skills in sorted(skills_by_year.items()) if skills}
    max_skills = max((len(skills) for skills in sorted_skills.values()), default=0)

    return sorted_skills, max_skills

def get_salary_stats_and_counts():
    jobs = JobListing.objects.values('published_at', 'salary_from', 'salary_to')
    salary_stats = defaultdict(lambda: {'min_salary': float('inf'), 'max_salary': float('-inf'), 'job_counts': int(0)})

    for job in jobs:
        year = job['published_at'].year
        salary_min = job['salary_from']
        salary_max = job['salary_to']

        # Обновляем минимальную и максимальную зарплату
        if salary_min:
            salary_stats[year]['min_salary'] = min(salary_stats[year]['min_salary'], salary_min)
        if salary_max:
            salary_stats[year]['max_salary'] = max(salary_stats[year]['max_salary'], salary_max)

        # Считаем количество вакансий
        salary_stats[year]['job_counts'] += 1

    # Преобразуем инфинити в None для корректного вывода
    for year in salary_stats:
        if salary_stats[year]['min_salary'] == float('inf'):
            salary_stats[year]['min_salary'] = None
        if salary_stats[year]['max_salary'] == float('-inf'):
            salary_stats[year]['max_salary'] = None

    return dict(salary_stats)

def get_salary_stats_and_counts_by_area():
    jobs = JobListing.objects.values('area_name', 'salary_from', 'salary_to')
    salary_stats = defaultdict(lambda: {'min_salary': float('inf'), 'max_salary': float('-inf'), 'job_counts': int(0)})

    for job in jobs:
        area = job['area_name']
        salary_min = job['salary_from']
        salary_max = job['salary_to']

        # Обновляем минимальную и максимальную зарплату
        if salary_min:
            salary_stats[area]['min_salary'] = min(salary_stats[area]['min_salary'], salary_min)
        if salary_max:
            salary_stats[area]['max_salary'] = max(salary_stats[area]['max_salary'], salary_max)

        # Считаем количество вакансий
        salary_stats[area]['job_counts'] += 1

    # Преобразуем инфинити в None для корректного вывода
    for area in salary_stats:
        if salary_stats[area]['min_salary'] == float('inf'):
            salary_stats[area]['min_salary'] = None
        if salary_stats[area]['max_salary'] == float('-inf'):
            salary_stats[area]['max_salary'] = None
    sorted_salary_stats = dict(sorted(salary_stats.items(), key=lambda x: x[1]['job_counts'], reverse=True))
    return dict(sorted_salary_stats)

def filter_job_counts(salary_stats, areas, n):
    filtered_counts = {}
    other_count = 0

    for area in areas:
        count = salary_stats[area]['job_counts']
        if count >= n:
            filtered_counts[area] = count
        else:
            other_count += count  # Суммируем в "Другие"

    if other_count > 0:
        filtered_counts["Другие"] = other_count

    return filtered_counts

# Create your views here.
def hello(request):
    template = loader.get_template('home.html')
    context = {
        'title': 'Администратор баз данных — ключевая роль в мире IT',
    }
    return HttpResponse(template.render(context))

def stat(request):
    template = loader.get_template('stat.html')

    salary_stats_area = get_salary_stats_and_counts_by_area()

    # Разделяем данные по ключам
    areas = list(salary_stats_area.keys())
    job_counts = [salary_stats_area[area]['job_counts'] for area in areas]

    n = 15  # Пороговое значение

    filtered_counts_area = filter_job_counts(salary_stats_area, areas, n)

    salary_stats_years = get_salary_stats_and_counts()

    # Разделяем данные по ключам
    years = list(salary_stats_years.keys())
    #min_salary = [salary_stats_years[year]['min_salary'] for year in years]
    #max_salary = [salary_stats_years[year]['max_salary'] for year in years]
    job_counts_years = [salary_stats_years[year]['job_counts'] for year in years]


    skills_by_year, max_skills = get_unique_skills_by_year()

    context = {
        'title': 'Общая статистика',

        'areas': list(filtered_counts_area.keys()),
        'job_counts': list(filtered_counts_area.values()),

        'years': years,
        'job_counts_years': job_counts_years,

        'skills_by_year': skills_by_year,  # Передаем массив навыков в шаблон
        'max_skills_range': range(20)

        #'min_salary': min_salary,
        #'max_salary': max_salary,

    }


    return HttpResponse(template.render(context))

def demand(request):
    template = loader.get_template('demand.html')
    salary_stats = get_salary_stats_and_counts()

    # Разделяем данные по ключам
    years = list(salary_stats.keys())
    #min_salary = [salary_stats[year]['min_salary'] for year in years]
    #max_salary = [salary_stats[year]['max_salary'] for year in years]
    job_counts = [salary_stats[year]['job_counts'] for year in years]

    context = {
        'title': 'Востребованность',
        'salary_stats': salary_stats,
        'years': years,
        #'min_salary': min_salary,
        #'max_salary': max_salary,
        'job_counts': job_counts,
    }
    return HttpResponse(template.render(context))

def geo(request):
    template = loader.get_template('geo.html')
    salary_stats = get_salary_stats_and_counts_by_area()

    # Разделяем данные по ключам
    areas = list(salary_stats.keys())
    job_counts = [salary_stats[area]['job_counts'] for area in areas]

    n = 15  # Пороговое значение

    filtered_counts = filter_job_counts(salary_stats, areas, n)

    context = {
        'title': 'География',
        'salary_stats': salary_stats,
        'areas': list(filtered_counts.keys()),
        #'min_salary': min_salary,
        #'max_salary': max_salary,
        'job_counts': list(filtered_counts.values()),
    }
    return HttpResponse(template.render(context))

def skills(request):
     template = loader.get_template('skills.html')

     skills_by_year, max_skills = get_unique_skills_by_year()
     context = {
         'title': 'Навыки',
         'skills_by_year': skills_by_year,  # Передаем массив навыков в шаблон
         'max_skills_range': range(20)
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