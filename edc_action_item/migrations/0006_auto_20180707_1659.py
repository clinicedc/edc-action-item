# Generated by Django 2.0.7 on 2018-07-07 14:59

import _socket
import django.db.models.deletion
import django_revision.revision_field
import edc_model_fields.fields.hostname_modification_field
import edc_model_fields.fields.userfield
import edc_model_fields.fields.uuid_auto_field
import edc_utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("edc_action_item", "0005_auto_20180409_1005")]

    operations = [
        migrations.CreateModel(
            name="Action",
            fields=[
                (
                    "created",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "user_created",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    edc_model_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    edc_model_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("tracking_identifier", models.CharField(max_length=30, null=True)),
                ("subject_identifier", models.CharField(max_length=50)),
                (
                    "parent_reference_identifier",
                    models.CharField(max_length=30, null=True),
                ),
                (
                    "related_reference_identifier",
                    models.CharField(max_length=30, null=True),
                ),
                ("action_identifier", models.CharField(max_length=25, unique=True)),
                (
                    "report_datetime",
                    models.DateTimeField(default=edc_utils.date.get_utcnow),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AlterModelOptions(
            name="historicalactionitem",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Action Item",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalactionitemupdate",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical action item update",
            },
        ),
        migrations.RenameField(
            model_name="actiontype", old_name="model", new_name="reference_model"
        ),
        migrations.AddField(
            model_name="actionitem",
            name="linked_to_reference",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name="historicalactionitem",
            name="linked_to_reference",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name="actionitem",
            name="parent_reference_identifier",
            field=models.CharField(
                blank=True,
                help_text="May be left blank. e.g. action identifier from reference model that opened the item (parent).",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="actionitem",
            name="reference_identifier",
            field=models.CharField(
                help_text="e.g. action identifier updated from the reference model",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="actionitem",
            name="related_reference_identifier",
            field=models.CharField(
                blank=True,
                help_text="May be left blank. e.g. action identifier from source model that opened the item.",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalactionitem",
            name="parent_action_item",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AlterField(
            model_name="historicalactionitem",
            name="parent_reference_identifier",
            field=models.CharField(
                blank=True,
                help_text="May be left blank. e.g. action identifier from reference model that opened the item (parent).",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalactionitem",
            name="reference_identifier",
            field=models.CharField(
                help_text="e.g. action identifier updated from the reference model",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalactionitem",
            name="related_reference_identifier",
            field=models.CharField(
                blank=True,
                help_text="May be left blank. e.g. action identifier from source model that opened the item.",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="actionitem",
            unique_together={("subject_identifier", "action_type", "action_identifier")},
        ),
        migrations.AddField(
            model_name="action",
            name="action_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="action",
                to="edc_action_item.ActionType",
                verbose_name="Action",
            ),
        ),
    ]
