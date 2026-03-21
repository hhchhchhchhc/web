import base64
import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone as dt_timezone
from pathlib import Path

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class WeChatPayConfigError(RuntimeError):
    pass


class WeChatPayAPIError(RuntimeError):
    def __init__(self, message, status_code=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


@dataclass
class WeChatPayConfig:
    mchid: str
    appid: str
    serial_no: str
    api_v3_key: str
    private_key_path: Path
    public_key_id: str
    public_key_path: Path
    notify_url: str
    base_url: str = 'https://api.mch.weixin.qq.com'


def _load_private_key(path: Path):
    return serialization.load_pem_private_key(path.read_bytes(), password=None)


def _load_public_key(path: Path):
    return serialization.load_pem_public_key(path.read_bytes())


def load_config() -> WeChatPayConfig:
    mchid = os.getenv('WECHAT_PAY_MCHID', '').strip()
    appid = os.getenv('WECHAT_PAY_APPID', '').strip()
    serial_no = os.getenv('WECHAT_PAY_SERIAL_NO', '').strip()
    api_v3_key = os.getenv('WECHAT_PAY_API_V3_KEY', '').strip()
    private_key_path = Path(os.getenv('WECHAT_PAY_PRIVATE_KEY_PATH', '')).expanduser()
    public_key_id = os.getenv('WECHAT_PAY_PUBLIC_KEY_ID', '').strip()
    public_key_path = Path(os.getenv('WECHAT_PAY_PUBLIC_KEY_PATH', '')).expanduser()
    notify_url = os.getenv('WECHAT_PAY_NOTIFY_URL', '').strip()

    required = {
        'WECHAT_PAY_MCHID': mchid,
        'WECHAT_PAY_APPID': appid,
        'WECHAT_PAY_SERIAL_NO': serial_no,
        'WECHAT_PAY_API_V3_KEY': api_v3_key,
        'WECHAT_PAY_PRIVATE_KEY_PATH': str(private_key_path),
        'WECHAT_PAY_PUBLIC_KEY_ID': public_key_id,
        'WECHAT_PAY_PUBLIC_KEY_PATH': str(public_key_path),
        'WECHAT_PAY_NOTIFY_URL': notify_url,
    }
    missing = [key for key, value in required.items() if not value or value == '.']
    if missing:
        raise WeChatPayConfigError(f'缺少微信支付配置: {", ".join(missing)}')
    if not private_key_path.exists():
        raise WeChatPayConfigError(f'微信支付商户私钥不存在: {private_key_path}')
    if not public_key_path.exists():
        raise WeChatPayConfigError(f'微信支付公钥不存在: {public_key_path}')

    return WeChatPayConfig(
        mchid=mchid,
        appid=appid,
        serial_no=serial_no,
        api_v3_key=api_v3_key,
        private_key_path=private_key_path,
        public_key_id=public_key_id,
        public_key_path=public_key_path,
        notify_url=notify_url,
    )


class WeChatPayClient:
    def __init__(self, config: WeChatPayConfig | None = None):
        self.config = config or load_config()
        self.private_key = _load_private_key(self.config.private_key_path)
        self.public_key = _load_public_key(self.config.public_key_path)

    def _build_authorization(self, method: str, canonical_url: str, body: str) -> str:
        nonce_str = uuid.uuid4().hex
        timestamp = str(int(time.time()))
        message = f'{method}\n{canonical_url}\n{timestamp}\n{nonce_str}\n{body}\n'
        signature = base64.b64encode(
            self.private_key.sign(
                message.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        ).decode('utf-8')
        return (
            'WECHATPAY2-SHA256-RSA2048 '
            f'mchid="{self.config.mchid}",'
            f'nonce_str="{nonce_str}",'
            f'signature="{signature}",'
            f'timestamp="{timestamp}",'
            f'serial_no="{self.config.serial_no}"'
        )

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        body = json.dumps(payload, ensure_ascii=False, separators=(',', ':')) if payload is not None else ''
        headers = {
            'Authorization': self._build_authorization(method, path, body),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'tool_aggregator/1.0',
        }
        url = f'{self.config.base_url}{path}'
        response = requests.request(method, url, data=body.encode('utf-8') if body else None, headers=headers, timeout=15)
        if response.status_code >= 400:
            raise WeChatPayAPIError(
                f'微信支付请求失败: {response.status_code}',
                status_code=response.status_code,
                body=response.text,
            )
        if not response.text:
            return {}
        return response.json()

    def create_native_order(self, order_no: str, description: str, amount_yuan: str, attach: str = '') -> dict:
        amount_fen = int(round(float(amount_yuan) * 100))
        payload = {
            'appid': self.config.appid,
            'mchid': self.config.mchid,
            'description': description[:127],
            'out_trade_no': order_no,
            'notify_url': self.config.notify_url,
            'attach': attach[:127],
            'time_expire': (datetime.now(dt_timezone.utc) + timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            'amount': {
                'total': amount_fen,
                'currency': 'CNY',
            },
        }
        return self._request('POST', '/v3/pay/transactions/native', payload)

    def query_order(self, order_no: str) -> dict:
        path = f'/v3/pay/transactions/out-trade-no/{order_no}?mchid={self.config.mchid}'
        return self._request('GET', path)

    def verify_notification(self, headers: dict, body: bytes) -> None:
        timestamp = headers.get('Wechatpay-Timestamp', '')
        nonce = headers.get('Wechatpay-Nonce', '')
        signature = headers.get('Wechatpay-Signature', '')
        serial = headers.get('Wechatpay-Serial', '')
        if not all([timestamp, nonce, signature, serial]):
            raise WeChatPayAPIError('微信支付回调请求头不完整')

        if serial != self.config.public_key_id:
            raise WeChatPayAPIError('微信支付公钥ID不匹配')

        message = f'{timestamp}\n{nonce}\n{body.decode("utf-8")}\n'.encode('utf-8')
        decoded_signature = base64.b64decode(signature)
        self.public_key.verify(
            decoded_signature,
            message,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )

    def decrypt_notification(self, body: bytes) -> dict:
        payload = json.loads(body.decode('utf-8'))
        resource = payload['resource']
        ciphertext = base64.b64decode(resource['ciphertext'])
        nonce = resource['nonce'].encode('utf-8')
        associated_data = resource.get('associated_data', '').encode('utf-8')
        aesgcm = AESGCM(self.config.api_v3_key.encode('utf-8'))
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
        return json.loads(plaintext.decode('utf-8'))
