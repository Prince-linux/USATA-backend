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


class Survey(models.Model):
    email = models.EmailField(default="test@example.com")
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1–5 scale

    # Rating before and after session
    understanding_before = models.IntegerField(choices=RATING_CHOICES, verbose_name="Understanding of African procurement before session")
    understanding_after = models.IntegerField(choices=RATING_CHOICES, verbose_name="Understanding of African procurement after session")

    # Open text questions
    most_valuable_topics = models.TextField(verbose_name="Which topics were most valuable?")
    what_to_learn_next = models.TextField(verbose_name="What do you want to learn in the next webinar?", blank=True)
    likely_to_register_future = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)
    
    # Confidence & interest fields
    confidence_in_next_steps = models.TextField(verbose_name="What are your next steps? How confident do you feel?", blank=True)
    interested_in_advisory = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)

    # Pricing feedback
    pricing_sensitivity = models.TextField(verbose_name="What would make this workshop worth paying for in the future?")

    # Future speaker interest
    willing_to_speak = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)

    # Timestamp
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey - {self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"


    
