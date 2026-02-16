# Generated manually
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='分类名称')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='URL标识')),
                ('description', models.TextField(blank=True, verbose_name='分类描述')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='工具名称')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='URL标识')),
                ('short_description', models.CharField(max_length=300, verbose_name='简短描述')),
                ('full_description', models.TextField(verbose_name='完整描述')),
                ('website_url', models.URLField(verbose_name='工具网站')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='tool_logos/', verbose_name='Logo')),
                ('is_featured', models.BooleanField(default=False, verbose_name='是否精选')),
                ('is_published', models.BooleanField(default=True, verbose_name='是否发布')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tools', to='tools.category', verbose_name='分类')),
            ],
            options={
                'verbose_name': '工具',
                'verbose_name_plural': '工具',
                'ordering': ['-created_at'],
            },
        ),
    ]
