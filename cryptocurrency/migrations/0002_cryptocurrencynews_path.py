# Generated by Django 4.0.5 on 2022-06-15 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrencynews',
            name='path',
            field=models.CharField(default=None, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
