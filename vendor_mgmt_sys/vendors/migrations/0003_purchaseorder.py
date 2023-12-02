# Generated by Django 4.2.7 on 2023-12-02 20:28

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_alter_vendor_average_response_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.UUIDField(default=uuid.uuid4, editable=False, help_text='unique identifier for purchase order', unique=True)),
                ('order_date', models.DateTimeField(auto_now_add=True, help_text='date and time when the order was placed')),
                ('delivery_date', models.DateTimeField(default=datetime.datetime(2023, 12, 6, 1, 58, 37, 116657), help_text='expected or actual delivery date')),
                ('items', models.JSONField(help_text='items included in the order')),
                ('quantity', models.IntegerField(help_text='total quantity of items ordered')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('cancelled', 'cancelled')], default='pending', help_text='current status of the order', max_length=10)),
                ('quality_rating', models.FloatField(help_text='rating for the order', null=True)),
                ('issue_date', models.DateTimeField(auto_now_add=True, help_text='date when the order was issued to the vendor')),
                ('acknowledgment_date', models.DateTimeField(help_text='date when the order was acknowledged by the vendor', null=True)),
                ('vendor', models.ForeignKey(help_text='vendor associated with the purchase order', on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
        ),
    ]
