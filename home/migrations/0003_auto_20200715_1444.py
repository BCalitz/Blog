# Generated by Django 3.0.6 on 2020-07-15 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200715_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='home.Author'),
        ),
    ]
