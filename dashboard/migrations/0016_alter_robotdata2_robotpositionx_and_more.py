# Generated by Django 4.0.3 on 2022-12-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_alter_robotdata2_robotpositionx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotdata2',
            name='robotPositionX',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='robotdata2',
            name='robotPositionY',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
