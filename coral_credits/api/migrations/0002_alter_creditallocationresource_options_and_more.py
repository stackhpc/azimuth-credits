# Generated by Django 5.0.1 on 2024-02-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="creditallocationresource",
            options={"ordering": ("allocation__start",)},
        ),
        migrations.AlterModelOptions(
            name="resourceconsumptionrecord",
            options={"ordering": ("consumer__start",)},
        ),
        migrations.AlterField(
            model_name="creditallocationresource",
            name="resource_hours",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="resourceconsumptionrecord",
            name="resource_hours",
            field=models.FloatField(),
        ),
    ]