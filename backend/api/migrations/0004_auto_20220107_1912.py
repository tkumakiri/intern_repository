# Generated by Django 2.2.26 on 2022-01-07 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20220107_1901'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='good',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_good'),
        ),
    ]