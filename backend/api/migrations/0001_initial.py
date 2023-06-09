# Generated by Django 4.2 on 2023-04-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=100)),
                ('definition', models.CharField(max_length=100)),
                ('timestamp', models.IntegerField(default=0)),
                ('maxtimesince', models.IntegerField(default=0)),
                ('lasttimesince', models.IntegerField(default=0)),
                ('right', models.IntegerField(default=0)),
                ('wrong', models.IntegerField(default=0)),
                ('lasteval', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data', models.JSONField(blank=True, null=True)),
                ('cache', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OldDeck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.JSONField(blank=True, null=True)),
                ('cache', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
