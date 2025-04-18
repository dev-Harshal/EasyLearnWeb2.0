# Generated by Django 5.1.8 on 2025-04-04 11:02

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('profile_photo', models.ImageField(null=True, upload_to='profile_photos/')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('institute', models.CharField(default='SSVPS', max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Student', 'Student'), ('Teacher', 'Teacher')], max_length=10)),
                ('joined_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Users Table',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\d{10}$')])),
                ('experience', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('department', models.CharField(choices=[('Admin Department', 'Admin Department'), ('Computer Engineering', 'Computer Engineering'), ('Civil Engineering', 'Civil Engineering'), ('Electronics Engineering', 'Electronics Engineering'), ('Management Studies', 'Management Studies')], default='Admin Department', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Profiles Table',
            },
        ),
    ]
