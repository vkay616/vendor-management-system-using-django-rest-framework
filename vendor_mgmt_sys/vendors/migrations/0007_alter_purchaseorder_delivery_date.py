# Generated by Django 4.2.7 on 2023-12-03 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0006_alter_purchaseorder_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 6, 15, 17, 39, 93617), help_text='expected or actual delivery date'),
        ),
    ]
