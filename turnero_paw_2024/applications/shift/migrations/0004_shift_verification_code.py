# Generated by Django 4.2.9 on 2024-06-29 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shift', '0003_shift_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='verification_code',
            field=models.CharField(default='', max_length=6),
        ),
    ]
