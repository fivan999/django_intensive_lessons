# Generated by Django 3.2.16 on 2023-03-31 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_shopuser_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuser',
            name='items',
        ),
    ]