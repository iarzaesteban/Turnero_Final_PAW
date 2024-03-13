# Generated by Django 4.2.9 on 2024-02-07 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('loggin', models.BooleanField(default=False)),
                ('start_time_attention', models.TimeField(blank=True, null=True)),
                ('end_time_attention', models.TimeField(blank=True, null=True)),
                ('picture', models.BinaryField()),
                ('id_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.person')),
            ],
        ),
    ]
