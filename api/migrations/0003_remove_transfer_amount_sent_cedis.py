# Generated by Django 4.0.1 on 2022-08-12 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_transfer_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfer',
            name='amount_sent_cedis',
        ),
    ]