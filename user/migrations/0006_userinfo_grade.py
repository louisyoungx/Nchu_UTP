# Generated by Django 3.0.5 on 2020-09-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200822_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='grade',
            field=models.CharField(blank=True, max_length=5, verbose_name='年级'),
        ),
    ]
