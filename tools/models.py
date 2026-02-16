from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """工具分类模型"""
    name = models.CharField('分类名称', max_length=100, unique=True)
    slug = models.SlugField('URL标识', max_length=100, unique=True, blank=True)
    description = models.TextField('分类描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        app_label = 'tools'
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tool(models.Model):
    """工具模型"""
    name = models.CharField('工具名称', max_length=200)
    slug = models.SlugField('URL标识', max_length=200, unique=True, blank=True)
    short_description = models.CharField('简短描述', max_length=300)
    full_description = models.TextField('完整描述')
    website_url = models.URLField('工具网站')
    logo = models.ImageField('Logo', upload_to='tool_logos/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tools',
        verbose_name='分类'
    )
    is_featured = models.BooleanField('是否精选', default=False)
    is_published = models.BooleanField('是否发布', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        app_label = 'tools'
        verbose_name = '工具'
        verbose_name_plural = '工具'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
