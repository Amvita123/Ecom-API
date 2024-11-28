# Generated by Django 5.1.3 on 2024-11-26 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_order_status_address_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('shiped', 'Shiped'), ('delivered', 'delivered'), ('cancelled', 'Cancelled'), ('Order Successful Complete', 'Order Successful Complete')], default='pending', max_length=30),
        ),
    ]
