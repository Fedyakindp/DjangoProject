from django.db import migrations, models
import csv
import os
from django.conf import settings

CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'vacancies_2024.csv')  # Файл должен быть в корне проекта

def load_csv_data(apps, schema_editor):
    JobListing = apps.get_model('jobinfo', 'JobListing')  # Подставьте название вашего приложения
    
    with open(CSV_FILE_PATH, 'rb') as file:
        raw_data = file.read()
        if raw_data.startswith(b'\xef\xbb\xbf'):
            raw_data = raw_data[3:]  # Удаляем BOM
        decoded_data = raw_data.decode('utf-8')

    with open(CSV_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write(decoded_data)

    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        records = (
            JobListing(
                name=row['name'],
                key_skills=row['key_skills'],
                salary_from=float(row['salary_from']) if row['salary_from'] else None,
                salary_to=float(row['salary_to']) if row['salary_to'] else None,
                salary_currency=row['salary_currency'],
                area_name=row['area_name'],
                published_at=row['published_at'],
            )
            for row in reader if 'database administrator' in row['name'].lower()
        )
        JobListing.objects.bulk_create(records)  # Загружаем данные одной операцией

class Migration(migrations.Migration):
    '''dependencies = [
        ('jobinfo', '__init__.py'),  # Замените на актуальную миграцию
    ]'''

    operations = [
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('key_skills', models.TextField()),
                ('salary_from', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_to', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_currency', models.CharField(max_length=10)),
                ('area_name', models.CharField(max_length=255)),
                ('published_at', models.DateTimeField()),
            ],
        ),
        migrations.RunPython(load_csv_data),
    ]
