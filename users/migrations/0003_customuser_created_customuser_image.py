# Generated by Django 4.0.10 on 2023-02-22 22:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_pic'),
        ),
    ]
