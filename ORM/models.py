from django.db import models


class SystemText(models.Model):
    menu = models.CharField(max_length=100)
    text = models.TextField()

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    is_bot = models.BooleanField(null=True)
    is_premium = models.BooleanField(null=True)
    language_code = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    instagram = models.CharField(max_length=255, null=True)

    date_added = models.BigIntegerField(null=True)

    is_banned = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)
    accepts_client_questions = models.BooleanField(default=False)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=255, null=True)