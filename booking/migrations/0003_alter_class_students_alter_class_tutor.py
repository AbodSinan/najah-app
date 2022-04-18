# Generated by Django 4.0.4 on 2022-04-18 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_profile_remove_tutor_education_level_and_more'),
        ('booking', '0002_class_rate_per_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(null=True, related_name='classes_joined', to='profile.profile'),
        ),
        migrations.AlterField(
            model_name='class',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='classes_tutored', to='profile.profile'),
        ),
    ]
