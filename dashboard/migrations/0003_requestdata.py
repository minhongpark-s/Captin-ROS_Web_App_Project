# Generated by Django 4.0.3 on 2022-11-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_robotdata2'),
    ]

    operations = [
        migrations.CreateModel(
            name='requestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestPosition', models.IntegerField()),
                ('requestMethod', models.IntegerField()),
                ('requestTime', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
