# Generated by Django 4.1.4 on 2022-12-11 17:56

import ckeditor.fields
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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image')),
                ('youtube_account', models.URLField(blank=True, null=True)),
                ('instagram_account', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('body', ckeditor.fields.RichTextField()),
                ('blog_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(blank=True, max_length=1000)),
                ('likes', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date_time'],
            },
        ),
    ]
