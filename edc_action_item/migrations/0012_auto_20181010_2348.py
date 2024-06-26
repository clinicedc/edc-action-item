# Generated by Django 2.1 on 2018-10-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("edc_action_item", "0011_auto_20181009_2236")]

    operations = [
        migrations.AlterField(
            model_name="reference",
            name="parent_action_identifier",
            field=models.CharField(
                help_text="action identifier that links to parent reference model instance.",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="reference",
            name="related_action_identifier",
            field=models.CharField(
                help_text="action identifier that links to related reference model instance.",
                max_length=30,
                null=True,
            ),
        ),
    ]
