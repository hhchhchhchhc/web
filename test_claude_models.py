#!/usr/bin/env python
import requests
import json

# API配置
base_url = "https://anyrouter.top"
api_key = "sk-4dRhBRszAgIZV1FrTktLbzidN56FtRnUegjOkkwSUTJFb1go"

# 测试多个模型
models_to_test = [
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "claude-3-5-sonnet-20241022"
]

print("正在测试不同的Claude模型...\n")

for model in models_to_test:
    print(f"测试模型: {model}")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": model,
        "max_tokens": 50,
        "messages": [
            {
                "role": "user",
                "content": "Say 'OK'"
            }
        ]
    }

    try:
        response = requests.post(
            f"{base_url}/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            content = result.get('content', [{}])[0].get('text', '')
            print(f"  ✓ 成功！响应: {content}")
        else:
            error_msg = response.json().get('error', {}).get('message', response.text)
            print(f"  ✗ 失败: {error_msg[:100]}")

    except Exception as e:
        print(f"  ✗ 错误: {str(e)[:100]}")

    print()
