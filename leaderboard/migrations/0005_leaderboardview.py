# Generated by Django 3.0.4 on 2020-04-04 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0004_auto_20200403_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaderBoardView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'leaderboard_view',
                'managed': False,
            },
        ),
    ]
