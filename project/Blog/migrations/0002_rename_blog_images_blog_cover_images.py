# Generated by Django 4.1.4 on 2022-12-21 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='blog_images',
            new_name='cover_images',
        ),
    ]