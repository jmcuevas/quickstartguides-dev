# Generated by Django 3.1.1 on 2020-10-31 20:02

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20201024_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
