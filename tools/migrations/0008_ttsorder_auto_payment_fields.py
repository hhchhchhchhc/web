import secrets
from django.db import migrations, models


def populate_payment_note_tokens(apps, schema_editor):
    TTSOrder = apps.get_model('tools', 'TTSOrder')
    used_tokens = set(
        TTSOrder.objects.exclude(payment_note_token='').values_list('payment_note_token', flat=True)
    )
    for order in TTSOrder.objects.filter(payment_note_token='').iterator():
        token = ''
        while not token or token in used_tokens:
            token = secrets.token_hex(3).upper()
        order.payment_note_token = token
        order.save(update_fields=['payment_note_token'])
        used_tokens.add(token)


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0007_ttsorder_payment_proof_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttsorder',
            name='payment_callback_payload',
            field=models.JSONField(blank=True, null=True, verbose_name='支付回调载荷'),
        ),
        migrations.AddField(
            model_name='ttsorder',
            name='payment_note_token',
            field=models.CharField(blank=True, default='', max_length=12, verbose_name='付款备注码'),
        ),
        migrations.AddField(
            model_name='ttsorder',
            name='payment_provider',
            field=models.CharField(blank=True, choices=[('alipay', '支付宝'), ('wechat', '微信支付')], max_length=16, verbose_name='支付渠道'),
        ),
        migrations.AddField(
            model_name='ttsorder',
            name='payment_reference',
            field=models.CharField(blank=True, max_length=80, verbose_name='渠道流水号'),
        ),
        migrations.AddField(
            model_name='ttsorder',
            name='payment_verified_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='支付核验时间'),
        ),
        migrations.RunPython(populate_payment_note_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='ttsorder',
            name='payment_note_token',
            field=models.CharField(blank=True, max_length=12, unique=True, verbose_name='付款备注码'),
        ),
    ]
