# Generated by Django 4.2 on 2023-05-13 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_post_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='price',
        ),
    ]