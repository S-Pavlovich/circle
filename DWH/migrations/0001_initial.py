# Generated by Django 4.1.5 on 2023-01-09 18:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_start_circle', models.DateField(blank=True, null=True)),
                ('telegram_id', models.IntegerField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_event', models.DateField()),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('additional_comment', models.TextField(blank=True, max_length=300, null=True, validators=[django.core.validators.MinLengthValidator(1)])),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DWH.user')),
            ],
        ),
    ]
