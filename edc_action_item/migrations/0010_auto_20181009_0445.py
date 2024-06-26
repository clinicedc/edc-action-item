# Generated by Django 2.1 on 2018-10-09 02:45

import django.db.models.deletion
from django.db import migrations, models

import edc_action_item.models.action_item


class Migration(migrations.Migration):
    dependencies = [("edc_action_item", "0009_auto_20180927_0306")]

    operations = [
        migrations.AlterModelManagers(
            name="actionitem",
            managers=[
                ("on_site", edc_action_item.models.action_item.CurrentSiteManager()),
                ("objects", edc_action_item.models.action_item.ActionItemManager()),
            ],
        ),
        migrations.RemoveField(model_name="actionitem", name="parent_reference_model"),
        migrations.RemoveField(
            model_name="historicalactionitem", name="parent_reference_model"
        ),
        migrations.AddField(
            model_name="actionitem",
            name="related_action_item",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AddField(
            model_name="historicalactionitem",
            name="related_action_item",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AddField(
            model_name="reference",
            name="action_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AddField(
            model_name="reference",
            name="parent_action_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AddField(
            model_name="reference",
            name="related_action_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AlterField(
            model_name="actionitem",
            name="action_identifier",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="actionitem",
            name="parent_action_item",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AlterField(
            model_name="historicalactionitem",
            name="action_identifier",
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
