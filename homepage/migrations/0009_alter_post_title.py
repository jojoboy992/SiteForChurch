# Generated by Django 5.1.1 on 2024-10-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_alter_post_content_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Maximum 30 characters.', max_length=20),
        ),
    ]
