# Generated by Django 5.0.7 on 2024-07-18 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myserver', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
