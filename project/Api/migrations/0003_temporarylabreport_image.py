# Generated by Django 5.0.4 on 2024-07-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0002_labreport_hospital_address_labreport_ocr_conf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporarylabreport',
            name='image',
            field=models.ImageField(null=True, upload_to='temp_lab_img'),
        ),
    ]
