# Generated by Django 2.2 on 2019-05-25 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='abouQuestion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='QA.Question'),
        ),
    ]
