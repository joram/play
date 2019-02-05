# Generated by Django 2.0.10 on 2019-02-05 17:47

from django.db import migrations, models
import django.db.models.deletion
import util.fields
import util.time


class Migration(migrations.Migration):

    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Snake",
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
                ("name", models.CharField(max_length=128)),
                ("url", models.CharField(max_length=128)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.Profile"
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]