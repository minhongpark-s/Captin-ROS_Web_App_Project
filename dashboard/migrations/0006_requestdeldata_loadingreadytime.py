# Generated by Django 4.0.3 on 2022-12-08 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_requestdeldata_referencestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestdeldata',
            name='loadingReadyTime',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
