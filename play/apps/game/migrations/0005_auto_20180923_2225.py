# Generated by Django 2.0.3 on 2018-09-23 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("snake", "0001_initial"), ("game", "0004_add_team_to_game")]

    operations = [
        migrations.AlterUniqueTogether(
            name="gamesnake", unique_together={("snake", "game")}
        )
    ]
