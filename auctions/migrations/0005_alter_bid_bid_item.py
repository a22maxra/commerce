# Generated by Django 4.0.4 on 2022-05-27 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BidItems', to='auctions.listing'),
        ),
    ]