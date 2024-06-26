# Generated by Django 5.0.1 on 2024-02-07 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CreditAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("email", models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name="ResourceClass",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="ResourceProvider",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("email", models.EmailField(max_length=254)),
                ("info_url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Consumer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("consume_ref", models.CharField(max_length=200)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="api.creditaccount",
                    ),
                ),
                (
                    "resource_provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="api.resourceprovider",
                    ),
                ),
            ],
            options={
                "unique_together": {("consume_ref", "resource_provider")},
            },
        ),
        migrations.CreateModel(
            name="CreditAllocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="api.creditaccount",
                    ),
                ),
            ],
            options={
                "unique_together": {("account", "start"), ("name", "account")},
            },
        ),
        migrations.CreateModel(
            name="CreditAllocationResource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "resource_hours",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "allocation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.creditallocation",
                    ),
                ),
                (
                    "resource_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="api.resourceclass",
                    ),
                ),
            ],
            options={
                "unique_together": {("allocation", "resource_class")},
            },
        ),
        migrations.CreateModel(
            name="ResourceConsumptionRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "resource_hours",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "consumer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.consumer"
                    ),
                ),
                (
                    "resource_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="api.resourceclass",
                    ),
                ),
            ],
            options={
                "unique_together": {("consumer", "resource_class")},
            },
        ),
    ]