# Generated by Django 5.1.5 on 2025-02-05 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0010_alter_plants_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='plants/upload/'),
        ),
    ]
