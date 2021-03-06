# Generated by Django 3.0.4 on 2020-03-27 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaderBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('rating', models.FloatField()),
                ('date_time', models.DateTimeField()),
            ],
            options={
                'ordering': ('rating', 'date_time')
            },
        ),
    ]
