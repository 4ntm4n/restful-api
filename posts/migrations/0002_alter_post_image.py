# Generated by Django 3.2.16 on 2023-01-15 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='../default_post_vn5qdm', upload_to='images/'),
        ),
    ]
