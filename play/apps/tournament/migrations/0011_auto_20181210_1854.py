# Generated by Django 2.0.3 on 2018-12-10 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("tournament", "0010_auto_20181210_1842")]

    operations = [
        migrations.RenameField(
            model_name="tournamentbracket",
            old_name="tournament_group",
            new_name="tournament",
        )
    ]
