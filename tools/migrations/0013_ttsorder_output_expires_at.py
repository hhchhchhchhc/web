from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0012_ttscreditaccount_is_unlimited'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttsorder',
            name='output_expires_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='音频过期时间'),
        ),
    ]
