from django.conf import settings
from django.db import migrations, models


def enable_unlimited_and_backfill(apps, schema_editor):
    TTSCreditAccount = apps.get_model('tools', 'TTSCreditAccount')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    TTSCreditAccount.objects.update(is_unlimited=True)

    existing_user_ids = set(TTSCreditAccount.objects.values_list('user_id', flat=True))
    missing_accounts = [
        TTSCreditAccount(user_id=user_id, is_unlimited=True)
        for user_id in User.objects.exclude(id__in=existing_user_ids).values_list('id', flat=True)
    ]
    if missing_accounts:
        TTSCreditAccount.objects.bulk_create(missing_accounts, batch_size=500)


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0016_alter_ttsorder_voice_preset_default_serena'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttscreditaccount',
            name='is_unlimited',
            field=models.BooleanField(default=True, verbose_name='是否无限额度'),
        ),
        migrations.RunPython(enable_unlimited_and_backfill, migrations.RunPython.noop),
    ]
