# Generated by Django 5.0.6 on 2024-05-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_category_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=25),
        ),
    ]
