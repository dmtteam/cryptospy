# Generated by Django 4.0.2 on 2022-05-06 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0019_twitterhashtags_mode_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userwallet',
            old_name='minimum_outcome_to_spy',
            new_name='maximum_income_to_spy',
        ),
        migrations.RenameField(
            model_name='userwalletrequest',
            old_name='minimum_outcome_to_spy',
            new_name='maximum_income_to_spy',
        ),
    ]
