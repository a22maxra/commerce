# Generated by Django 4.0.4 on 2022-05-29 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]