# Generated by Django 5.0.3 on 2024-04-25 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_user_is_guard"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_guard",
            field=models.BooleanField(default=False, verbose_name="Es Guardia?"),
        ),
    ]