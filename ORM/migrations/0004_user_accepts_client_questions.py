# Generated by Django 5.0.6 on 2024-05-10 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORM', '0003_user_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accepts_client_questions',
            field=models.BooleanField(default=False),
        ),
    ]
