# Generated by Django 5.1 on 2024-08-30 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_alter_invoice_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='billing_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
