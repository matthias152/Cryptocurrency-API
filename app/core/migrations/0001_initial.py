# Generated by Django 3.2.14 on 2022-07-28 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('quantity', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('walletid', models.CharField(max_length=35)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_created', models.DateField()),
                ('time_created', models.TimeField()),
                ('type', models.CharField(max_length=30)),
                ('quantityCrypto', models.FloatField()),
                ('price', models.FloatField()),
                ('balance_after', models.FloatField()),
                ('cryptocurrency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cryptocurrency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('walletid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.walletid')),
            ],
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='walletid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.walletid'),
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
