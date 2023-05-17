# Generated by Django 2.1 on 2018-09-27 01:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_action_item", "0008_auto_20180809_0303")]

    operations = [
        migrations.AddField(
            model_name="actionitem",
            name="emailed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="actionitem",
            name="emailed_datetime",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="historicalactionitem",
            name="emailed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="historicalactionitem",
            name="emailed_datetime",
            field=models.DateTimeField(null=True),
        ),
    ]
