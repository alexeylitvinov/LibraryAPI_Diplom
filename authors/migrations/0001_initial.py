# Generated by Django 4.2.9 on 2024-08-10 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('surname', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('text', models.TextField(blank=True, null=True, verbose_name='О авторе')),
                ('slug', models.SlugField(unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'db_table': 'authors',
            },
        ),
    ]
