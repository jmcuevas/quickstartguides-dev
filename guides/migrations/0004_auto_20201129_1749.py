# Generated by Django 3.1.1 on 2020-11-29 17:49

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0003_guide_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]