# Generated by Django 4.2.7 on 2023-12-29 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_reviewrating_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
