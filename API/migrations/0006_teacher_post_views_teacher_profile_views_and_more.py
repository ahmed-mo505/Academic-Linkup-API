# Generated by Django 5.0.2 on 2024-05-02 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_student_about_student_friend_list_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='post_views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='profile_views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='university',
            name='university_auth_file',
            field=models.FileField(blank=True, null=True, upload_to='university_files'),
        ),
    ]
