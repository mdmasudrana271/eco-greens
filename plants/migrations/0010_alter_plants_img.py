# Generated by Django 5.1.5 on 2025-02-03 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0009_alter_plants_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='img',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
