# Generated by Django 2.0.3 on 2018-07-19 13:46

from django.db import migrations, models
import django.db.models.deletion
import util.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [("snake", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    util.fields.ShortUUIDField(
                        max_length=128, primary_key=True, serialize=False
                    ),
                ),
                ("engine_id", models.CharField(max_length=128, null=True)),
                ("status", models.CharField(default="pending", max_length=30)),
                ("turn", models.IntegerField(default=0)),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
                ("food", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="GameSnake",
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
                ("death", models.CharField(default="pending", max_length=128)),
                ("turns", models.IntegerField(default=0)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="game.Game"
                    ),
                ),
                (
                    "snake",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="snake.Snake"
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="gamesnake", unique_together={("snake", "game")}
        ),
    ]
