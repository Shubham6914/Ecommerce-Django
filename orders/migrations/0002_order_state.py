# Generated by Django 4.2.7 on 2023-12-25 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(default='Default State', max_length=20),
        ),
    ]