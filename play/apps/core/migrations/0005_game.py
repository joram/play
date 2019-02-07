# Generated by Django 2.0.10 on 2019-02-07 07:56

from django.db import migrations, models
import util.fields
import util.time


class Migration(migrations.Migration):

    dependencies = [("core", "0004_profile_optin_marketing")]

    operations = [
        migrations.CreateModel(
            name="Game",
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
                ("engine_id", models.CharField(max_length=128, null=True)),
                ("status", models.CharField(default="pending", max_length=30)),
                ("turn", models.IntegerField(default=0)),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
                ("max_turns_to_next_food_spawn", models.IntegerField(default=15)),
                ("snakes", models.ManyToManyField(to="core.Snake")),
            ],
            options={"abstract": False},
        )
    ]
