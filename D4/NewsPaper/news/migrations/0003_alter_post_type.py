# Generated by Django 4.1 on 2022-08-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_rename_category_name_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('NW', 'news'), ('AR', 'article')], default='NW', max_length=2),
        ),
    ]
