# Generated by Django 5.0.6 on 2024-05-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_remove_studentextra_enrollment_book_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(default='Title', max_length=100),
        ),
    ]