# Generated by Django 2.0.10 on 2019-02-07 22:21

from django.db import migrations, models
import django.db.models.deletion
import util.fields
import util.time


class Migration(migrations.Migration):

    dependencies = [("core", "0006_snake_is_public")]

    operations = [
        migrations.CreateModel(
            name="GameSnake",
            fields=[
                (
                    "created",
                    util.fields.CreatedDateTimeField(
                        blank=True, default=util.time.now, editable=False
                    ),
                ),
                (
                    "modified",
                    util.fields.ModifiedDateTimeField(
                        blank=True, default=util.time.now, editable=False
                    ),
                ),
                (
                    "id",
                    util.fields.ShortUUIDField(
                        max_length=128, primary_key=True, serialize=False
                    ),
                ),
                ("death", models.CharField(default="pending", max_length=128)),
                ("turns", models.IntegerField(default=0)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.Game"
                    ),
                ),
                (
                    "snake",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.Snake"
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
