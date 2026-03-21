#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup

html_file = os.path.expanduser('~/图片/bookmarks_2026_2_5.html')

with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

root_dl = soup.find('dl')
print(f"找到根DL: {root_dl is not None}")

if root_dl:
    # 查看DL的所有子元素
    children = list(root_dl.children)
    print(f"根DL的子元素数量: {len(children)}")

    for i, child in enumerate(children[:10]):
        if hasattr(child, 'name'):
            print(f"子元素 {i}: {child.name}")

    # 尝试不使用recursive=False
    dts = root_dl.find_all('dt')
    print(f"\n所有DT数量(递归): {len(dts)}")

    # 找H3
    h3s = root_dl.find_all('h3')
    print(f"所有H3数量: {len(h3s)}")
    if h3s:
        print(f"第一个H3: {h3s[0].get_text(strip=True)}")

