from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Tool, Category, TopicPage

class ToolSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Tool.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None

    def location(self, obj):
        return reverse('tool_detail', kwargs={'slug': obj.slug})

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f"{reverse('tool_list')}?category={obj.slug}"

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return [
            'home',
            'topic_list',
            'trending_tools',
            'trending_columns',
            'tts_studio',
            'free_resources',
            'openclaw_column',
            'algorithm_geek_column',
            'quant_column',
            'psychology_column',
            'nano_banana_pro_guide',
            'side_hustle_japan_goods',
            'side_hustle_xiaohongshu_virtual_store_matrix',
            'quant_article_tushare',
            'openclaw_miniqmt_trading_guide',
            'openclaw_a_share_auto_trading_guide',
            'openclaw_guardian_agent_guide',
            'openclaw_ai_learning_workflow_guide',
        ]

    def location(self, item):
        return reverse(item)


class TopicSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return TopicPage.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('topic_detail', kwargs={'slug': obj.slug})
