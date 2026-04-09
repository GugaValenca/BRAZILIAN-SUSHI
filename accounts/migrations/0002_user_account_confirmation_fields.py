import uuid

from django.db import migrations, models
from django.utils import timezone


def populate_account_confirmation_fields(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    now = timezone.now()

    for user in User.objects.all().iterator():
        if not user.account_confirmation_token:
            user.account_confirmation_token = uuid.uuid4()
        if user.is_active and not user.account_confirmed_at:
            user.account_confirmed_at = now
        user.save(update_fields=["account_confirmation_token", "account_confirmed_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="account_confirmation_sent_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="account_confirmation_token",
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="account_confirmed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(populate_account_confirmation_fields, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="user",
            name="account_confirmation_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
