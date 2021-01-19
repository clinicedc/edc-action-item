# Generated by Django 3.0.9 on 2021-01-19 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_action_item', '0026_auto_20200729_2240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actiontype',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'export', 'import'), 'get_latest_by': 'modified', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='reference',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'export', 'import'), 'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
    ]