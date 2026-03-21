from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tools.models import Category, TopicPage


INTENT_PATTERNS = [
    ("入门指南", "新手快速上手，低门槛高效率"),
    ("高效工作流", "围绕真实工作流筛选可落地工具组合"),
    ("免费可用", "优先可免费使用或低成本试用的工具"),
]


class Command(BaseCommand):
    help = "按分类自动生成/更新专题页（程序化SEO）"

    def handle(self, *args, **options):
        created = 0
        updated = 0

        categories = Category.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.WARNING("没有分类数据，无法生成专题页。"))
            return

        for category in categories:
            for suffix, value_prop in INTENT_PATTERNS:
                title = f"{category.name}{suffix} AI工具专题"
                slug = slugify(f"{category.slug}-{suffix}", allow_unicode=True)
                meta_description = (
                    f"{category.name}方向工具精选。{value_prop}，"
                    f"覆盖真实场景与热门产品，持续自动更新。"
                )
                intro = (
                    f"本专题聚焦「{category.name}」场景，"
                    f"按热度、可用性和上手速度整理工具，减少试错成本。"
                )

                topic, is_created = TopicPage.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "title": title,
                        "meta_description": meta_description,
                        "intro": intro,
                        "is_published": True,
                    },
                )
                topic.categories.set([category])

                if is_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"专题页生成完成：新增 {created}，更新 {updated}，总分类 {categories.count()}。"
            )
        )
