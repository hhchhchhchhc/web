from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0013_ttsorder_output_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttsorder',
            name='cancel_requested',
            field=models.BooleanField(default=False, verbose_name='已请求取消'),
        ),
    ]
