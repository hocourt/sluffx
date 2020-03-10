# Generated by Django 3.0.2 on 2020-03-08 19:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_content', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sitesettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_site', models.BooleanField(default=True)),
                ('advert', models.TextField(blank=True, null=True)),
                ('contact_info', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.IntegerField()),
                ('reversevideo', models.BooleanField(default=False)),
                ('datecolor', models.CharField(default='black', max_length=20)),
                ('detailcolor', models.CharField(default='#0000C0', max_length=20)),
                ('attendeescolor', models.CharField(default='#00C000', max_length=20)),
                ('backgroundcolor', models.CharField(default='#F3FFF3', max_length=20)),
                ('datecolor_rev', models.CharField(default='white', max_length=20)),
                ('detailcolor_rev', models.CharField(default='aqua', max_length=20)),
                ('attendeescolor_rev', models.CharField(default='lawngreen', max_length=20)),
                ('backgroundcolor_rev', models.CharField(default='black', max_length=20)),
                ('photo_cover', models.ImageField(null=True, upload_to='images/')),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=100)),
                ('is_live', models.BooleanField(default=True)),
                ('title', models.TextField(null=True)),
                ('cover', models.ImageField(null=True, upload_to='images/')),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authorp', to='users.Person')),
            ],
        ),
    ]