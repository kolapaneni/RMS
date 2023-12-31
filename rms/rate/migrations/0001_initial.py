# Generated by Django 4.2.5 on 2023-09-23 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('discount_id', models.IntegerField()),
                ('discount_name', models.CharField(max_length=255)),
                ('discount_type', models.CharField(choices=[('fixed', 'Fixed'), ('percentage', 'Percentage')], max_length=10)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('room_id', models.IntegerField()),
                ('room_name', models.CharField(max_length=255)),
                ('default_rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiscountRoomRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate.discount')),
                ('room_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate.roomrate')),
            ],
        ),
        migrations.CreateModel(
            name='OverriddenRoomRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('overridden_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stay_date', models.DateField()),
                ('room_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate.roomrate')),
            ],
            options={
                'unique_together': {('room_rate', 'stay_date')},
            },
        ),
    ]
