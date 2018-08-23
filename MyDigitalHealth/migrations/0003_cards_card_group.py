# Generated by Django 2.0.5 on 2018-08-04 04:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MyDigitalHealth', '0002_auto_20180523_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='card_group',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.PROTECT, to='MyDigitalHealth.Category'),
            preserve_default=False,
        ),
    ]
