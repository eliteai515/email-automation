# Generated by Django 4.0.4 on 2023-10-26 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automail', '0017_blacklistedemaildomains'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcampaigntemplate',
            name='failed_emails',
            field=models.TextField(blank=True, default='', max_length=4000, null=True),
        ),
    ]
