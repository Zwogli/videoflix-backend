# Generated by Django 5.0.7 on 2024-07-12 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_authentication', '0002_customuser_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='username',
            new_name='user_name',
        ),
    ]