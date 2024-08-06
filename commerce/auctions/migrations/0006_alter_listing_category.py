# Generated by Django 5.0.3 on 2024-08-06 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_update_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Furniture', 'Furinture'), ('Clothes', 'Clothes'), ('Sports', 'Sports'), ('Toys', 'Toys'), ('Technology', 'Technology'), ('Pet', 'Pet'), ('Food', 'Food'), ('Other', 'Other')], default='Other', max_length=64),
        ),
    ]