# Generated by Django 4.1.5 on 2023-01-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DWH', '0006_alter_user_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='timezone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]