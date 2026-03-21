import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "向搜索引擎主动提交 sitemap"

    def add_arguments(self, parser):
        parser.add_argument(
            "--site",
            default="https://ai-tool.indevs.in",
            help="站点域名，例如 https://ai-tool.indevs.in",
        )
        parser.add_argument(
            "--indexnow-key",
            default=os.getenv("INDEXNOW_KEY", ""),
            help="IndexNow key（可选），不传则仅验证 sitemap 可访问",
        )
        parser.add_argument(
            "--key-location",
            default=os.getenv("INDEXNOW_KEY_LOCATION", ""),
            help="IndexNow key 文件 URL（可选）。若未传则默认使用 /<key>.txt",
        )

    def handle(self, *args, **options):
        site = options["site"].rstrip("/")
        indexnow_key = options["indexnow_key"].strip()
        key_location = options["key_location"].strip()
        sitemap_url = f"{site}/sitemap.xml"

        if getattr(settings, "DEBUG", False):
            self.stdout.write(self.style.WARNING("当前为 DEBUG 模式，继续执行。"))

        sitemap_req = Request(
            sitemap_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; IndexNowBot/1.0)"},
        )
        try:
            with urlopen(sitemap_req, timeout=20) as response:
                code = response.getcode()
                self.stdout.write(self.style.SUCCESS(f"sitemap 可访问: {sitemap_url} -> {code}"))
        except (HTTPError, URLError, TimeoutError) as exc:
            self.stdout.write(self.style.WARNING(f"sitemap 访问异常: {sitemap_url} -> {exc}，继续尝试 IndexNow 提交"))

        if not indexnow_key:
            self.stdout.write(
                self.style.WARNING(
                    "未提供 INDEXNOW_KEY，已跳过 IndexNow 提交。"
                )
            )
            self.stdout.write(
                "提示：Google/Bing 旧 ping 接口已废弃，建议配置 IndexNow key。"
            )
            return

        payload = {
            "host": site.replace("https://", "").replace("http://", ""),
            "key": indexnow_key,
            "urlList": [site, sitemap_url],
        }
        if key_location:
            payload["keyLocation"] = key_location
        else:
            payload["keyLocation"] = f"{site}/{indexnow_key}.txt"
        req = Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=20) as response:
                code = response.getcode()
                self.stdout.write(self.style.SUCCESS(f"IndexNow 提交成功 -> {code}"))
        except HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", errors="ignore")
            except Exception:
                detail = ""
            if detail:
                self.stdout.write(self.style.ERROR(f"IndexNow 提交失败 -> {exc} | {detail}"))
            else:
                self.stdout.write(self.style.ERROR(f"IndexNow 提交失败 -> {exc}"))
        except (URLError, TimeoutError) as exc:
            self.stdout.write(self.style.ERROR(f"IndexNow 提交失败 -> {exc}"))
