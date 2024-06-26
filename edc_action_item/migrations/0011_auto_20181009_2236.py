# Generated by Django 2.1 on 2018-10-09 02:45

import django.db.models.deletion
from django.db import migrations, models

import edc_action_item.models.action_item


class Migration(migrations.Migration):
    dependencies = [("edc_action_item", "0010_auto_20181009_0445")]

    operations = [
        migrations.RenameField(
            model_name="actionitem",
            old_name="parent_reference_identifier",
            new_name="parent_action_identifier",
        ),
        migrations.RenameField(
            model_name="actionitem",
            old_name="related_reference_identifier",
            new_name="related_action_identifier",
        ),
        migrations.RenameField(
            model_name="historicalactionitem",
            old_name="parent_reference_identifier",
            new_name="parent_action_identifier",
        ),
        migrations.RenameField(
            model_name="historicalactionitem",
            old_name="related_reference_identifier",
            new_name="related_action_identifier",
        ),
        migrations.RenameField(
            model_name="reference",
            old_name="parent_reference_identifier",
            new_name="parent_action_identifier",
        ),
        migrations.RenameField(
            model_name="reference",
            old_name="related_reference_identifier",
            new_name="related_action_identifier",
        ),
    ]
