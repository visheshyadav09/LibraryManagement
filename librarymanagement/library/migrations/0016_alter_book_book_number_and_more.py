# Generated by Django 5.0.6 on 2024-05-14 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_alter_issuedbook_expirydate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_number',
            field=models.CharField(default='123456', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='studentextra',
            name='student_number',
            field=models.CharField(default='123456', max_length=100, unique=True),
        ),
    ]
