# Generated by Django 5.0.4 on 2024-08-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0003_temporarylabreport_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='labreport',
            name='sample',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='labreport',
            name='test_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
