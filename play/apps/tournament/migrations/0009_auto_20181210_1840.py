# Generated by Django 2.0.3 on 2018-12-10 18:40

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False
    dependencies = [
        ("snake", "0001_initial"),
        ("tournament", "0008_auto_20181128_2153"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SnakeTournament", new_name="SnakeTournamentBracket"
        ),
        migrations.RenameModel(old_name="Tournament", new_name="TournamentBracket"),
    ]
