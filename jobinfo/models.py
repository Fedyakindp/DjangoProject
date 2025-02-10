from django.db import models

class JobListing(models.Model):
    name = models.CharField(max_length=255)
    key_skills = models.TextField()
    salary_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10)
    area_name = models.CharField(max_length=255)
    published_at = models.DateTimeField()
