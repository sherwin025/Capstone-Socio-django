# Generated by Django 4.0.3 on 2022-03-08 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socioapi', '0002_rename_zipzode_member_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessevent',
            name='title',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
