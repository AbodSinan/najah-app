from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0009_populate_uuid_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]

