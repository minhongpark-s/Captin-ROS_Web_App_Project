# Generated by Django 4.0.3 on 2022-12-10 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_requestdeldata_urtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestdeldata',
            name='UCTime',
            field=models.CharField(max_length=20, null=True),
        ),
    ]