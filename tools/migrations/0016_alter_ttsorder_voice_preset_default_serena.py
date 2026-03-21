from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0015_columnpage_alter_ttsorder_voice_preset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttsorder',
            name='voice_preset',
            field=models.CharField(
                choices=[
                    ('aiden', 'Aiden'),
                    ('dylan', 'Dylan'),
                    ('eric', 'Eric'),
                    ('ono_anna', 'Ono_anna'),
                    ('ryan', 'Ryan'),
                    ('serena', 'Serena'),
                    ('sohee', 'Sohee'),
                    ('uncle_fu', 'Uncle_fu'),
                    ('vivian', 'Vivian'),
                    ('sweet_vivian', '旧版预设：Vivian'),
                    ('gentle_serena', '旧版预设：Serena'),
                    ('youthful_ono', '旧版预设：Ono_anna'),
                    ('custom', '旧版预设：定制风格'),
                ],
                default='serena',
                max_length=32,
                verbose_name='音色方案',
            ),
        ),
    ]
