# Generated by Django 3.0.7 on 2020-06-17 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotest', '0008_auto_20200616_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_file',
            field=models.FileField(default='.txt', upload_to='testt', verbose_name='Document File'),
        ),
    ]
