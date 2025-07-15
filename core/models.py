from django.db import models

class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    company_address = models.TextField()
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    interested_countries = models.JSONField()  # Stores list of strings
    created_at = models.DateTimeField(auto_now_add=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    has_bid_before = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)
    participation_barriers = models.TextField(blank=True, null=True)
    current_tools = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
