# Generated by Django 3.0.8 on 2020-10-30 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20201030_1035'),
        ('order', '0005_auto_20201030_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='product',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.ProductItem'),
        ),
    ]
