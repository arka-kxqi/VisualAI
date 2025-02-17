# Generated by Django 5.0.4 on 2024-07-30 13:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='labreport',
            name='hospital_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labreport',
            name='ocr_conf',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='labreportimage',
            name='image',
            field=models.ImageField(upload_to='lab_reports'),
        ),
        migrations.CreateModel(
            name='TemporaryLabReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocr_text', models.TextField(blank=True, null=True)),
                ('gemini_prompt1_response', models.TextField(blank=True, null=True)),
                ('original_report_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ocr_confidence', models.TextField(blank=True, null=True)),
                ('address_of_hospital', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_lab_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
