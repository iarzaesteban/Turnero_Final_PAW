# Generated by Django 4.2.9 on 2024-03-05 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_password_hash_users_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='picture',
            field=models.BinaryField(editable=True, null=True),
        ),
    ]
