# Generated by Django 2.2.26 on 2022-01-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='data',
            field=models.TextField(null=True, verbose_name='画像データ'),
        ),
        migrations.AddField(
            model_name='user',
            name='image_name',
            field=models.CharField(max_length=200, null=True, verbose_name='画像名'),
        ),
    ]