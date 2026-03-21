#!/usr/bin/env python
import requests
import json

# API配置
base_url = "https://anyrouter.top"
api_key = "sk-4dRhBRszAgIZV1FrTktLbzidN56FtRnUegjOkkwSUTJFb1go"

# 测试API
print("正在测试Claude API连接...\n")

# 尝试调用API
headers = {
    "Content-Type": "application/json",
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01"
}

# 简单的测试消息
data = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 100,
    "messages": [
        {
            "role": "user",
            "content": "Hello, please respond with 'API is working'"
        }
    ]
}

try:
    # 发送请求
    response = requests.post(
        f"{base_url}/v1/messages",
        headers=headers,
        json=data,
        timeout=30
    )

    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}\n")

    if response.status_code == 200:
        result = response.json()
        print("✓ API连接成功！")
        print(f"\n响应内容:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"✗ API调用失败")
        print(f"错误信息: {response.text}")

except requests.exceptions.Timeout:
    print("✗ 请求超时")
except requests.exceptions.ConnectionError:
    print("✗ 连接失败，无法访问API端点")
except Exception as e:
    print(f"✗ 发生错误: {str(e)}")
