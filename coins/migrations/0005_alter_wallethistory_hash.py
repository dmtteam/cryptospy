# Generated by Django 4.0.2 on 2022-03-24 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0004_wallethistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallethistory',
            name='hash',
            field=models.CharField(max_length=150),
        ),
    ]
