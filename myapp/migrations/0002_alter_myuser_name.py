# Generated by Django 5.0.4 on 2024-04-16 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
