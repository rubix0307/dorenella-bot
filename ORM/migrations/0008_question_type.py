# Generated by Django 5.0.6 on 2024-05-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ORM', '0007_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
