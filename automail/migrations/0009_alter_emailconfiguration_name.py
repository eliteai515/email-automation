# Generated by Django 4.0.4 on 2023-10-05 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automail', '0008_emailconfiguration_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfiguration',
            name='name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
