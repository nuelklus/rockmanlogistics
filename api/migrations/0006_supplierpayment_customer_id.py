# Generated by Django 4.0.1 on 2022-03-19 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierpayment',
            name='customer_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.customer'),
        ),
    ]