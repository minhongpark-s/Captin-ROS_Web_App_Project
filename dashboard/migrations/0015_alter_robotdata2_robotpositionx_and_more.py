# Generated by Django 4.0.3 on 2022-12-11 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_rename_referencetime_requestdeldata_mstime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotdata2',
            name='robotPositionX',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='robotdata2',
            name='robotPositionY',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]
