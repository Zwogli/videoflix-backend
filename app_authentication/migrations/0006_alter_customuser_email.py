# Generated by Django 5.0.7 on 2024-08-02 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_authentication', '0005_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]