# Generated by Django 2.1.7 on 2019-03-21 20:09

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
            name='Corgi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('age_years', models.IntegerField(default=0)),
                ('age_months', models.IntegerField(default=0)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('X', 'Other')], default='X', max_length=1)),
                ('coloring', models.CharField(choices=[('red', 'Red'), ('rh-tc', 'Red-Headed Tricolor'), ('bh-tc', 'Black-Headed Tricolor'), ('sable', 'Sable'), ('fawn', 'Fawn'), ('other', 'Other')], default='red', max_length=5)),
                ('city', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=300)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
