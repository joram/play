# Generated by Django 2.0.3 on 2019-01-19 23:07

from django.db import migrations, models
import django.db.models.deletion
import util.fields
import util.time


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('snake', '0002_auto_20181213_0150'),
        ('game', '0010_merge_20181221_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLeaderboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', util.fields.CreatedDateTimeField(blank=True, default=util.time.now, editable=False)),
                ('modified', util.fields.ModifiedDateTimeField(blank=True, default=util.time.now, editable=False)),
                ('game', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.Game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaderboardResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', util.fields.CreatedDateTimeField(blank=True, default=util.time.now, editable=False)),
                ('modified', util.fields.ModifiedDateTimeField(blank=True, default=util.time.now, editable=False)),
                ('mu_change', models.FloatField()),
                ('sigma_change', models.FloatField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSnakeLeaderboard',
            fields=[
                ('created', util.fields.CreatedDateTimeField(blank=True, default=util.time.now, editable=False)),
                ('modified', util.fields.ModifiedDateTimeField(blank=True, default=util.time.now, editable=False)),
                ('user_snake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='snake.UserSnake')),
                ('mu', models.FloatField(null=True)),
                ('sigma', models.FloatField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='leaderboardresult',
            name='snake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaderboard.UserSnakeLeaderboard'),
        ),
    ]
