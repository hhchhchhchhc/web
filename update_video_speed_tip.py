#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

tool = Tool.objects.get(slug='ai-video-speed-watching')
tool.short_description = '使用剪映生成字幕+PotPlayer倍速播放，或飞书妙记3~16倍速看视频'
tool.full_description = '''快速看视频的高效方法：

**方法一：剪映+PotPlayer（推荐）**
1. 下载视频
2. 上传到免费版剪映
3. 输入视频→输出带字幕视频 ✅
4. 使用本地PotPlayer进行3~16倍速播放

**方法二：飞书妙记**
1. 下载视频
2. 上传到飞书妙记
3. 使用3~16倍速播放
4. 配合字幕观看

注意：千问倍速播放极其卡顿，不推荐使用。这个方法特别适合学习课程视频、会议录像等需要快速获取信息的场景。'''
tool.website_url = 'https://www.capcut.cn/'
tool.save()

print("✅ 已更新工具：AI加速看视频方法")
