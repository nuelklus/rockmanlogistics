# Generated by Django 4.0.1 on 2022-08-14 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_transfer_amount_sent_cedis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfer',
            name='balance',
        ),
    ]