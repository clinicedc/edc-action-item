# Generated by Django 2.1 on 2018-08-09 03:03

import _socket
import django.db.models.deletion
import django_audit_fields.fields.uuid_auto_field
import django_revision.revision_field
import edc_model_fields.fields.hostname_modification_field
import edc_model_fields.fields.userfield
import edc_utils
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_action_item", "0007_auto_20180707_1715")]

    operations = [
        migrations.CreateModel(
            name="Reference",
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
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
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
                (
                    "action_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="action",
                        to="edc_action_item.ActionType",
                        verbose_name="Action",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.RemoveField(model_name="action", name="action_type"),
        migrations.AlterField(
            model_name="actionitem",
            name="linked_to_reference",
            field=models.BooleanField(
                default=False,
                editable=False,
                help_text='True if this action is linked to it\'s reference_model.Initially False if this action is created before reference_model.Always True when reference_model creates the action.Set to True when reference_model is created and "links" to this action.(Note: reference_model looks for actions where linked_to_reference is False before attempting to create a new ActionItem).',
            ),
        ),
        migrations.AlterField(
            model_name="historicalactionitem",
            name="linked_to_reference",
            field=models.BooleanField(
                default=False,
                editable=False,
                help_text='True if this action is linked to it\'s reference_model.Initially False if this action is created before reference_model.Always True when reference_model creates the action.Set to True when reference_model is created and "links" to this action.(Note: reference_model looks for actions where linked_to_reference is False before attempting to create a new ActionItem).',
            ),
        ),
        migrations.AlterUniqueTogether(name="actionitem", unique_together=set()),
        migrations.DeleteModel(name="Action"),
    ]
