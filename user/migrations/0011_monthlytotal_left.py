# Generated by Django 3.2 on 2021-04-30 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_list_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlytotal',
            name='left',
            field=models.BigIntegerField(default=False),
        ),
    ]