# Generated by Django 2.2.6 on 2019-10-19 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20191019_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'verbose_name': 'Copy', 'verbose_name_plural': 'Book Copies'},
        ),
    ]
