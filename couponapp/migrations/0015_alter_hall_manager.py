# Generated by Django 4.1.1 on 2023-03-23 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('couponapp', '0014_alter_feastcoupon_feast'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='manager',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='couponapp.manager'),
        ),
    ]
