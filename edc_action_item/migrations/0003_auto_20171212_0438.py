# Generated by Django 2.0 on 2017-12-12 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_action_item', '0002_auto_20171212_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionitem',
            name='instructions',
            field=models.TextField(blank=True, help_text='populated by action class', null=True),
        ),
        migrations.AlterField(
            model_name='historicalactionitem',
            name='instructions',
            field=models.TextField(blank=True, help_text='populated by action class', null=True),
        ),
    ]
