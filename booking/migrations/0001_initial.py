# Generated by Django 4.0.4 on 2022-04-18 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0003_alter_educationlevel_is_higher_education'),
        ('profile', '0004_profile_remove_tutor_education_level_and_more'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('duration', models.DecimalField(decimal_places=2, max_digits=4)),
                ('frequency', models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')], max_length=1)),
                ('no_of_times', models.IntegerField()),
                ('education_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.educationlevel')),
                ('students', models.ManyToManyField(null=True, related_name='%(class)s_joined', to='profile.profile')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='education.subject')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_tutored', to='profile.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('booking_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='booking.class')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payment.payment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profile.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
