# Generated by Django 5.0.6 on 2024-05-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_author_remove_book_author_remove_book_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentextra',
            name='enrollment',
        ),
        migrations.AddField(
            model_name='book',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentextra',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
