#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

tool = Tool.objects.get(slug='ai-video-speed-watching')
tool.short_description = '使用百度网盘、飞书妙记或B站插件下载字幕，实现3~16倍速高效观看视频'
tool.full_description = '''快速看视频的高效方法：

**方法一：哔哩哔哩+插件（最便捷）**
1. 使用浏览器插件直接下载B站视频字幕
2. B站会AI自动生成字幕，无需自己上传生成
3. 本地播放器倍速观看

**方法二：百度网盘**
1. 下载视频
2. 上传到百度网盘
3. 在线观看，自动生成字幕
4. 使用3~16倍速播放

**方法三：飞书妙记**
1. 下载视频
2. 上传到飞书妙记
3. 使用3~16倍速播放
4. 配合字幕观看

这个方法特别适合学习课程视频、会议录像等需要快速获取信息的场景。'''
tool.save()

print("✅ 已更新工具：AI加速看视频方法")
