# Generated by Django 4.2.7 on 2023-12-04 05:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0008_alter_purchaseorder_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 7, 11, 14, 44, 32554), help_text='expected or actual delivery date'),
        ),
    ]
