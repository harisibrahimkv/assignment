# Generated by Django 4.2.3 on 2023-07-26 14:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("body", models.TextField(blank=True, null=True)),
                ("sender", models.CharField(blank=True, max_length=128, null=True)),
                ("receiver", models.CharField(blank=True, max_length=128, null=True)),
                ("subject", models.CharField(blank=True, max_length=256, null=True)),
                ("date", models.DateTimeField(blank=True, null=True)),
                ("message_id", models.CharField(max_length=512)),
            ],
        ),
    ]
