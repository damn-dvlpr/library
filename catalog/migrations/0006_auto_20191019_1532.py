# Generated by Django 2.2.6 on 2019-10-19 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20191018_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='initialized',
        ),
        migrations.AlterField(
            model_name='book',
            name='number_of_copies',
            field=models.IntegerField(default=0, help_text='Number of copies of this book. Leave this field untouched.'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='copies', to='catalog.Book'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.CharField(help_text='Unique id across whole library for this book.', max_length=250, primary_key=True, serialize=False),
        ),
    ]
