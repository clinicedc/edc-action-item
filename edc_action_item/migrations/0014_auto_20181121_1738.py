# Generated by Django 2.1.3 on 2018-11-21 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_action_item', '0013_auto_20181108_0353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionitemupdate',
            name='action_item',
        ),
        migrations.RemoveField(
            model_name='historicalactionitemupdate',
            name='action_item',
        ),
        migrations.RemoveField(
            model_name='historicalactionitemupdate',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='ActionItemUpdate',
        ),
        migrations.DeleteModel(
            name='HistoricalActionItemUpdate',
        ),
    ]