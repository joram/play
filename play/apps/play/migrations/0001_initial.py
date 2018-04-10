# Generated by Django 2.0.3 on 2018-04-10 22:29

import apps.play.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', apps.play.fields.ShortUUIDField(max_length=128, primary_key=True, serialize=False)),
                ('team_id', models.CharField(max_length=128)),
                ('is_bounty', models.BooleanField(default=False)),
                ('is_registration', models.BooleanField(default=False)),
                ('is_tournament', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
        ),
        migrations.CreateModel(
            name='Snake',
            fields=[
                ('id', apps.play.fields.ShortUUIDField(max_length=128, primary_key=True, serialize=False)),
                ('team_id', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('url', models.CharField(max_length=2084)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', apps.play.fields.ShortUUIDField(max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('tournament_snake_id', models.CharField(max_length=128)),
                ('tournament_bracket', models.CharField(max_length=128)),
            ],
        ),
    ]
