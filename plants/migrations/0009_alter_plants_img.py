# Generated by Django 5.1.5 on 2025-02-03 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0008_remove_plants_image_plants_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='plants/upload/'),
        ),
    ]
