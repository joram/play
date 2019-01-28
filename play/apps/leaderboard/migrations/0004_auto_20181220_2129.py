# Generated by Django 2.0.3 on 2018-12-20 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("leaderboard", "0003_auto_20181016_2142")]

    operations = [
        migrations.CreateModel(
            name="LeaderboardResult",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mu_change", models.FloatField()),
                ("sigma_change", models.FloatField()),
                (
                    "snake",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="leaderboard.UserSnakeLeaderboard",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="gameleaderboard",
            name="game",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to="game.Game",
            ),
        ),
    ]
