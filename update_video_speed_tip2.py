#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

tool = Tool.objects.get(slug='ai-video-speed-watching')
tool.short_description = '使用百度网盘或飞书妙记在线观看视频，支持字幕和3~16倍速播放'
tool.full_description = '''快速看视频的高效方法：

**方法一：百度网盘（推荐）**
1. 下载视频
2. 上传到百度网盘
3. 在线观看，自动生成字幕
4. 使用3~16倍速播放

**方法二：飞书妙记**
1. 下载视频
2. 上传到飞书妙记
3. 使用3~16倍速播放
4. 配合字幕观看

注意：剪映免费版只支持500多兆云空间，不够用。这个方法特别适合学习课程视频、会议录像等需要快速获取信息的场景。'''
tool.website_url = 'https://pan.baidu.com/'
tool.save()

print("✅ 已更新工具：AI加速看视频方法")
