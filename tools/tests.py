import os
import json
import hashlib
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import patch
import subprocess

import numpy as np
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import OperationalError as DBOperationalError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from zoneinfo import ZoneInfo

from tools import views as tool_views
from tools.models import ApiRelayService, UserApiRelayAccess, TushareNewsCache, TushareReplayLease, MassiveReplayCache, MassiveReplayLease, TardisRagEntry, TushareRagEntry, SocialRadarTask, CodexBriefingTask, TTSOrder, TTSCreditAccount, EdgeInferenceOffer, EdgeInferenceRequest
from tools.qwen_runtime import QwenTTSRuntime
from tools.management.commands.process_tts_orders import Command as ProcessTTSOrdersCommand
from tools.tardis_rag import extract_tardis_entries_from_text
from tools.social_radar_runtime import cleanup_expired_social_radar_results
from tools.tushare_rag import extract_tushare_entries_from_text
from tools.tts_config import estimate_total_chunks, get_tts_runtime_rules
from tools.tts_retention import get_special_archive_deadline, should_archive_special_tts


class TTSConfigTests(SimpleTestCase):
    def test_default_runtime_rules(self):
        with patch.dict(os.environ, {}, clear=True):
            rules = get_tts_runtime_rules()
            self.assertEqual(rules['direct_max_chars'], 800)
            self.assertEqual(rules['chunk_chars'], 400)
            self.assertEqual(rules['batch_chars'], 800)

    def test_estimate_total_chunks_uses_direct_threshold(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(estimate_total_chunks(700), 1)
            self.assertEqual(estimate_total_chunks(2172), 6)

    def test_special_archive_cutoff_uses_same_day_1000_shanghai(self):
        before_cutoff = datetime(2026, 3, 26, 1, 59, tzinfo=ZoneInfo('UTC'))
        at_cutoff = datetime(2026, 3, 26, 2, 0, tzinfo=ZoneInfo('UTC'))
        next_day_before_cutoff = datetime(2026, 3, 27, 1, 59, tzinfo=ZoneInfo('UTC'))

        self.assertEqual(
            get_special_archive_deadline(before_cutoff),
            datetime(2026, 3, 26, 10, 0, 0, tzinfo=ZoneInfo('Asia/Shanghai')),
        )
        self.assertTrue(should_archive_special_tts(before_cutoff))
        self.assertFalse(should_archive_special_tts(at_cutoff))
        self.assertTrue(should_archive_special_tts(next_day_before_cutoff))


class _FakeTalker:
    rope_deltas = 'sentinel'


class _FakeModel:
    def __init__(self):
        self.talker = _FakeTalker()


class _FakeTTS:
    def __init__(self, side_effect):
        self.model = _FakeModel()
        self._side_effect = side_effect
        self.calls = []

    def generate_custom_voice(self, **kwargs):
        self.calls.append(kwargs)
        return self._side_effect(**kwargs)


class QwenRuntimeBatchTests(SimpleTestCase):
    def test_generate_batch_audio_uses_true_batch_inference(self):
        runtime = QwenTTSRuntime()
        fake_tts = _FakeTTS(
            side_effect=lambda **kwargs: (
                [np.array([0.1], dtype=np.float32), np.array([0.2], dtype=np.float32)],
                24000,
            )
        )

        wavs, sr = runtime._generate_batch_audio(
            tts=fake_tts,
            batch_chunks=['第一段', '第二段'],
            language='Chinese',
            speaker='serena',
            instruct='保持自然',
            max_new_tokens=512,
        )

        self.assertEqual(sr, 24000)
        self.assertEqual(len(wavs), 2)
        self.assertEqual(len(fake_tts.calls), 1)
        self.assertEqual(fake_tts.calls[0]['text'], ['第一段', '第二段'])
        self.assertEqual(fake_tts.calls[0]['language'], ['Chinese', 'Chinese'])
        self.assertEqual(fake_tts.calls[0]['speaker'], ['serena', 'serena'])
        self.assertEqual(fake_tts.calls[0]['instruct'], ['保持自然', '保持自然'])
        self.assertIsNone(fake_tts.model.talker.rope_deltas)


class TTSWorkerCapacityTests(SimpleTestCase):
    @patch('tools.management.commands.process_tts_orders.torch.cuda.is_available', return_value=False)
    def test_gpu_capacity_allows_claim_when_cuda_unavailable(self, _mock_cuda_available):
        command = ProcessTTSOrdersCommand()
        self.assertTrue(command._gpu_has_capacity_for_more_orders(active_jobs=0, group_limit=1))
        self.assertFalse(command._gpu_has_capacity_for_more_orders(active_jobs=1, group_limit=1))

    @patch('tools.management.commands.process_tts_orders.torch.cuda.is_available', return_value=True)
    def test_gpu_capacity_blocks_claim_when_gpu_over_threshold(self, _mock_cuda_available):
        command = ProcessTTSOrdersCommand()

        class _FakeMem:
            used = 90
            total = 100

        class _FakeUtil:
            gpu = 95

        class _FakeNvml:
            @staticmethod
            def nvmlInit():
                return None

            @staticmethod
            def nvmlDeviceGetHandleByIndex(_index):
                return object()

            @staticmethod
            def nvmlDeviceGetUtilizationRates(_handle):
                return _FakeUtil()

            @staticmethod
            def nvmlDeviceGetMemoryInfo(_handle):
                return _FakeMem()

        with patch.dict('sys.modules', {'pynvml': _FakeNvml}):
            self.assertFalse(command._gpu_has_capacity_for_more_orders(active_jobs=0, group_limit=2))

    def test_generate_batch_audio_falls_back_to_serial_on_batch_error(self):
        progress_events = []

        def side_effect(**kwargs):
            texts = kwargs['text']
            if texts == ['第一段', '第二段']:
                raise RuntimeError('batch failed')
            if texts == ['第一段']:
                return [np.array([0.1], dtype=np.float32)], 24000
            if texts == ['第二段']:
                return [np.array([0.2], dtype=np.float32)], 24000
            raise AssertionError(f'unexpected texts: {texts}')

        runtime = QwenTTSRuntime()
        fake_tts = _FakeTTS(side_effect=side_effect)

        wavs, sr = runtime._generate_batch_audio(
            tts=fake_tts,
            batch_chunks=['第一段', '第二段'],
            language='Chinese',
            speaker='serena',
            instruct='保持自然',
            max_new_tokens=512,
            progress_callback=lambda phase, **payload: progress_events.append((phase, payload)),
            batch_index=1,
            total_batches=1,
        )

        self.assertEqual(sr, 24000)
        self.assertEqual(len(wavs), 2)
        self.assertEqual([call['text'] for call in fake_tts.calls], [['第一段', '第二段'], ['第一段'], ['第二段']])
        self.assertEqual(progress_events[0][0], 'batch_fallback')
        self.assertIn('batch_generation_error:RuntimeError', progress_events[0][1]['reason'])

    def test_generate_batch_items_returns_per_item_errors_after_batch_fallback(self):
        progress_events = []

        def side_effect(**kwargs):
            texts = kwargs['text']
            if texts == ['第一段', '第二段']:
                raise RuntimeError('batch failed')
            if texts == ['第一段']:
                return [np.array([0.1], dtype=np.float32)], 24000
            if texts == ['第二段']:
                raise ValueError('bad text')
            raise AssertionError(f'unexpected texts: {texts}')

        runtime = QwenTTSRuntime()
        fake_tts = _FakeTTS(side_effect=side_effect)
        runtime.tts = fake_tts

        results, sr = runtime.generate_batch_items(
            items=[
                {'text': '第一段', 'language': 'Chinese', 'speaker': 'serena', 'instruct': '保持自然', 'max_new_tokens': 512},
                {'text': '第二段', 'language': 'Chinese', 'speaker': 'serena', 'instruct': '保持自然', 'max_new_tokens': 512},
            ],
            progress_callback=lambda phase, **payload: progress_events.append((phase, payload)),
        )

        self.assertEqual(sr, 24000)
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[1], ValueError)
        self.assertEqual(progress_events[0][0], 'batch_fallback')


class ApiRelayTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='relayuser', email='relay@example.com', password='secret123')
        self.service = ApiRelayService.objects.create(
            slug='demo-api',
            name='Demo API',
            base_url='http://127.0.0.1:9001',
            is_active=True,
            require_api_key=True,
            require_login=False,
            require_manual_approval=True,
            allowed_methods='GET,POST',
            timeout_seconds=30,
            upstream_headers='{"Authorization":"Bearer upstream-secret","X-Upstream-Flag":"1"}',
            upstream_query_params='{"api_key":"abc123","fixed":"yes"}',
            public_path='/api-relay/demo-api/',
            description='demo',
            example_paths='/health\n/v1/items',
        )

    def test_api_relay_requires_api_key(self):
        response = self.client.get('/api-relay/demo-api/health')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], 'api_key_required')

    def test_api_relay_rejects_invalid_api_key(self):
        response = self.client.get('/api-relay/demo-api/health', HTTP_X_API_KEY='atk_badprefix.badsecret')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'invalid_api_key')

    @patch('tools.views.TushareReplayLease.objects.select_for_update')
    def test_tushare_replay_lease_claim_degrades_when_table_missing(self, mock_select_for_update):
        mock_select_for_update.return_value.filter.return_value.first.side_effect = DBOperationalError('no such table')
        is_leader, owner_token = tool_views._claim_tushare_replay_lease('k' * 64, 'pro/analyst_rank', 'year=2024')
        self.assertTrue(is_leader)
        self.assertEqual(owner_token, '')

    def test_api_relay_rejects_key_without_permission(self):
        access = UserApiRelayAccess.objects.create(user=self.user, service=self.service, is_enabled=False)
        raw_key = access.issue_api_key()
        access.save()
        response = self.client.get('/api-relay/demo-api/health', HTTP_X_API_KEY=raw_key)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'permission_denied')

    def test_massive_service_card_appears_in_api_relay_hub(self):
        tool_views._get_api_relay_service('massive')
        response = self.client.get('/api-relay/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Massive Flat Files Replay')
        self.assertContains(response, '/massive/')

    @patch('tools.views._get_massive_s3_client')
    def test_massive_proxy_caches_file_without_second_upstream_fetch(self, mock_client_factory):
        service = tool_views._get_api_relay_service('massive')
        key_user = User.objects.create_user(username='massive_file_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 27, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='massive_file_key',
            api_key_secret_hash=make_password('massive_file_key'),
            api_key_last4='file',
        )

        class _Stream:
            def __init__(self, payload):
                self.payload = payload
                self.sent = False

            def read(self, _size=-1):
                if self.sent:
                    return b''
                self.sent = True
                return self.payload

            def close(self):
                return None

        class _FakeClient:
            def __init__(self):
                self.calls = 0

            def get_object(self, **kwargs):
                self.calls += 1
                return {
                    'Body': _Stream(b'col1,col2\n1,2\n'),
                    'ContentType': 'application/gzip',
                    'ETag': '"etag-1"',
                }

        fake_client = _FakeClient()
        mock_client_factory.return_value = fake_client

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(tool_views, 'MASSIVE_REPLAY_CACHE_ROOT', Path(tmpdir)):
                response = self.client.get(
                    '/massive/file/us_stocks_sip/minute_aggs_v1/2023/01/2023-01-03.csv.gz',
                    HTTP_X_API_KEY='massive_file_key',
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
                self.assertEqual(b''.join(response.streaming_content), b'col1,col2\n1,2\n')
                self.assertEqual(fake_client.calls, 1)
                cache_entry = MassiveReplayCache.objects.get(relay_path='file/us_stocks_sip/minute_aggs_v1/2023/01/2023-01-03.csv.gz')
                self.assertEqual(cache_entry.cache_bucket, 'object_history')
                self.assertTrue(Path(cache_entry.body_path).exists())

                response = self.client.get(
                    '/massive/file/us_stocks_sip/minute_aggs_v1/2023/01/2023-01-03.csv.gz',
                    HTTP_X_API_KEY='massive_file_key',
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
                self.assertEqual(b''.join(response.streaming_content), b'col1,col2\n1,2\n')
                self.assertEqual(fake_client.calls, 1)

    @patch('tools.views._get_massive_s3_client')
    def test_massive_proxy_caches_missing_file_as_404(self, mock_client_factory):
        from botocore.exceptions import ClientError

        service = tool_views._get_api_relay_service('massive')
        key_user = User.objects.create_user(username='massive_missing_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 27, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='massive_missing_key',
            api_key_secret_hash=make_password('massive_missing_key'),
            api_key_last4='miss',
        )

        class _FakeClient:
            def __init__(self):
                self.calls = 0

            def get_object(self, **kwargs):
                self.calls += 1
                raise ClientError(
                    {
                        'Error': {'Code': 'NoSuchKey', 'Message': 'not found'},
                        'ResponseMetadata': {'HTTPStatusCode': 404},
                    },
                    'GetObject',
                )

        fake_client = _FakeClient()
        mock_client_factory.return_value = fake_client

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(tool_views, 'MASSIVE_REPLAY_CACHE_ROOT', Path(tmpdir)):
                response = self.client.get(
                    '/massive/file/us_stocks_sip/minute_aggs_v1/2023/01/2023-01-01.csv.gz',
                    HTTP_X_API_KEY='massive_missing_key',
                )
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
                self.assertEqual(fake_client.calls, 1)
                cache_entry = MassiveReplayCache.objects.get(relay_path='file/us_stocks_sip/minute_aggs_v1/2023/01/2023-01-01.csv.gz')
                self.assertEqual(cache_entry.cache_bucket, 'missing_object')

                response = self.client.get(
                    '/massive/file/us_stocks_sip/minute_aggs_v1/2023/01/2023-01-01.csv.gz',
                    HTTP_X_API_KEY='massive_missing_key',
                )
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
                self.assertEqual(fake_client.calls, 1)

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_api_relay_forwards_with_injected_headers_and_query(self, mock_request):
        access = UserApiRelayAccess.objects.create(
            user=self.user,
            service=self.service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 21, 12, 0, tzinfo=ZoneInfo('UTC')),
        )
        raw_key = access.issue_api_key()
        access.save()

        class _FakeResponse:
            status_code = 200
            content = b'{"ok": true}'
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()
        response = self.client.get(
            '/api-relay/demo-api/health',
            {'client_param': 'from-user', 'api_key': 'user-override-attempt'},
            HTTP_X_API_KEY=raw_key,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Service'], 'demo-api')
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs['url'], 'http://127.0.0.1:9001/health')
        self.assertEqual(kwargs['params']['client_param'], 'from-user')
        self.assertEqual(kwargs['params']['api_key'], 'abc123')
        self.assertEqual(kwargs['params']['fixed'], 'yes')
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer upstream-secret')
        self.assertEqual(kwargs['headers']['X-Upstream-Flag'], '1')
        self.assertEqual(kwargs['headers']['X-Ai-Tools-Username'], 'relayuser')
        self.assertNotIn('Cookie', kwargs['headers'])

    @patch('tools.views.RELAY_HTTP_SESSION.get')
    def test_quant_article_tushare_renders_catalog_examples(self, mock_get):
        class _CatalogResponse:
            ok = True

            @staticmethod
            def json():
                return {
                    'categories': {
                        '互动易问答（沪深）': ['irm_qa_sh'],
                        '公告数据': ['anns_d'],
                        '主连/连续合约数据': ['fut_mapping'],
                        '部分其他类型数据': ['trade_cal'],
                    },
                    'examples': {
                        '互动易问答（沪深）': [
                            {
                                'api_name': 'irm_qa_sh',
                                'params': {'ts_code': '600000.SH'},
                                'example_url': '/pro/irm_qa_sh?ts_code=600000.SH',
                            }
                        ],
                        '公告数据': [
                            {
                                'api_name': 'anns_d',
                                'params': {'ann_date': '20260327', 'ts_code': '000001.SZ'},
                                'example_url': '/pro/anns_d?ann_date=20260327&ts_code=000001.SZ',
                            }
                        ],
                        '主连/连续合约数据': [
                            {
                                'api_name': 'fut_mapping',
                                'params': {'ts_code': 'IF.CFX'},
                                'example_url': '/pro/fut_mapping?ts_code=IF.CFX',
                            }
                        ],
                        '部分其他类型数据': [
                            {
                                'api_name': 'trade_cal',
                                'params': {'exchange': 'SSE', 'start_date': '20260301', 'end_date': '20260331'},
                                'example_url': '/pro/trade_cal?exchange=SSE&start_date=20260301&end_date=20260331',
                            }
                        ],
                    },
                }

        mock_get.return_value = _CatalogResponse()
        response = self.client.get('/quant/tushare-pro-guide/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '站内可用目录与示例参数')
        self.assertContains(response, 'ETF 数据')
        self.assertContains(response, '2026-12-29')
        self.assertContains(response, 'irm_qa_sh')
        self.assertContains(response, 'fut_mapping')
        self.assertContains(response, 'trade_cal')
        self.assertContains(response, 'guide 已按 catalog 新目录同步')
        self.assertContains(response, '部分其他类型数据')
        self.assertContains(response, '/tushare/pro/irm_qa_sh?ts_code=600000.SH')
        self.assertContains(response, 'https://ai-tool.indevs.in/tushare/pro/express_news')
        self.assertContains(response, 'print(&quot;api_name=&quot;, &quot;express_news&quot;)')
        self.assertContains(response, 'https://ai-tool.indevs.in/tushare/pro/cjzc')
        self.assertContains(response, 'print(&quot;api_name=&quot;, &quot;cjzc&quot;)')
        self.assertNotContains(response, '/tushare/pro/anns_d?ann_date=20260327&amp;ts_code=000001.SZ')

    @patch('tools.views.RELAY_HTTP_SESSION.get')
    def test_quant_tushare_catalog_page_renders_searchable_directory(self, mock_get):
        class _CatalogResponse:
            ok = True

            @staticmethod
            def json():
                return {
                    'categories': {'融资融券基础数据': ['margin_detail'], '板块数据': ['concept', 'index_classify', 'index_member']},
                    'examples': {
                        '融资融券基础数据': [
                            {
                                'api_name': 'margin_detail',
                                'params': {'trade_date': '20260320', 'ts_code': '000002.SZ'},
                                'fields': 'trade_date,ts_code,name,rzye,rzmre',
                                'example_url': '/pro/margin_detail?trade_date=20260320&ts_code=000002.SZ',
                                'retention_policy': {
                                    'label': '通常到北京时间当日 24:00',
                                    'recommended_refresh': '交易日收盘后到晚间补齐阶段最值得刷新',
                                    'reason': '这类数据通常按日结算或按日披露，当日内重复值较高。',
                                },
                            }
                        ],
                        '板块数据': [
                            {
                                'api_name': 'concept',
                                'params': {'src': 'ts'},
                                'fields': 'code,name,src',
                                'example_url': '/pro/concept?src=ts',
                            },
                            {
                                'api_name': 'index_classify',
                                'params': {'level': 'L1', 'src': 'SW2021'},
                                'fields': 'index_code,industry_name,level,industry_code,is_pub,parent_code,src',
                                'example_url': '/pro/index_classify?src=SW2021&level=L1',
                            },
                            {
                                'api_name': 'index_member',
                                'params': {'index_code': '801010.SI'},
                                'fields': 'index_code,con_code,in_date,out_date,is_new',
                                'example_url': '/pro/index_member?index_code=801010.SI',
                            },
                        ],
                    },
                    'cache_policy': {'historical_date_queries': '通常 3 到 7 天'},
                }

        mock_get.return_value = _CatalogResponse()
        response = self.client.get('/quant/tushare-pro-catalog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '可搜索前端目录页')
        self.assertContains(response, 'margin_detail')
        self.assertContains(response, '推荐 fields')
        self.assertContains(response, '推荐保留周期')
        self.assertContains(response, '推荐访问节奏')
        self.assertContains(response, 'Python 示例')
        self.assertContains(response, 'import requests')
        self.assertContains(response, 'session.trust_env = False')
        self.assertContains(response, 'URL = &quot;https://ai-tool.indevs.in/tushare/pro/margin_detail&quot;')
        self.assertContains(response, '点击测试')
        self.assertContains(response, '/tushare/pro/margin_detail?trade_date=20260320&amp;ts_code=000002.SZ')
        self.assertContains(response, '分钟数据快速入口')
        self.assertContains(response, '/tushare/minute/000001.SZ/latest?freq=5MIN')
        self.assertContains(response, 'freq=60MIN')
        self.assertContains(response, '板块数据')
        self.assertContains(response, 'index_classify')
        self.assertContains(response, 'index_member')
        self.assertContains(response, 'express_news')
        self.assertContains(response, 'cjzc')
        self.assertContains(response, 'news_cctv')
        self.assertContains(response, 'news_economic_baidu')
        self.assertContains(response, 'news_report_time_baidu')
        self.assertContains(response, 'news_trade_notify_dividend_baidu')
        self.assertContains(response, 'news_trade_notify_suspend_baidu')
        self.assertContains(response, 'index_basic')
        self.assertContains(response, 'index_daily')
        self.assertContains(response, 'index_weekly')
        self.assertContains(response, 'index_monthly')
        self.assertContains(response, '/tushare/pro/index_daily?ts_code=000001.SH&amp;start_date=2026-03-01&amp;end_date=2026-03-27')
        self.assertContains(response, '/tushare/pro/index_weekly?ts_code=000001.SH&amp;start_date=2024-01-01&amp;end_date=2026-03-27')
        self.assertContains(response, '/tushare/pro/index_monthly?ts_code=000001.SH&amp;start_date=2018-01-01&amp;end_date=2026-03-27')
        self.assertContains(response, '分析师数据')
        self.assertContains(response, 'analyst_rank')
        self.assertContains(response, 'analyst_detail')
        self.assertContains(response, 'analyst_history')
        self.assertContains(response, '公告与研报')
        self.assertContains(response, 'stock_notice_report')
        self.assertContains(response, 'stock_zh_a_disclosure_report_cninfo')
        self.assertContains(response, 'research_report')
        self.assertContains(response, 'stock_research_report_em')
        self.assertContains(response, 'fund_announcement_report_em')

    @patch('tools.views.RELAY_HTTP_SESSION.get')
    def test_quant_tushare_catalog_page_renders_express_news_entry(self, mock_get):
        class _CatalogResponse:
            ok = True

            @staticmethod
            def json():
                return {
                    'categories': {},
                    'examples': {},
                    'cache_policy': {'historical_date_queries': '通常 3 到 7 天'},
                }

        mock_get.return_value = _CatalogResponse()
        response = self.client.get('/quant/tushare-pro-catalog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'express_news')
        self.assertContains(response, '站内补充快讯新闻口径')
        self.assertContains(response, '当前缓存 15 分钟，陈旧缓存 2 天内清理')
        self.assertContains(response, 'cjzc')
        self.assertContains(response, '站内补充东方财富财经早餐口径')
        self.assertContains(response, '当前缓存 12 小时，陈旧缓存 14 天内清理')
        self.assertContains(response, 'news_cctv')
        self.assertContains(response, '按日期回放')
        self.assertContains(response, '历史日线')
        self.assertContains(response, '历史周线')
        self.assertContains(response, '历史月线')
        self.assertContains(response, 'analyst_rank')
        self.assertContains(response, 'analyst_detail')
        self.assertContains(response, 'analyst_history')
        self.assertContains(response, 'research_report')
        self.assertContains(response, 'fund_announcement_report_em')

    @patch('tools.views.RELAY_HTTP_SESSION.get')
    def test_quant_tushare_catalog_groups_news_interfaces_together(self, mock_get):
        class _CatalogResponse:
            ok = True

            @staticmethod
            def json():
                return {
                    'categories': {},
                    'examples': {},
                    'cache_policy': {'historical_date_queries': '通常 3 到 7 天'},
                }

        mock_get.return_value = _CatalogResponse()
        response = self.client.get('/quant/tushare-pro-catalog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '新闻数据')
        self.assertContains(response, '/tushare/pro/express_news?scope=all&amp;limit=50')
        self.assertContains(response, '/tushare/pro/express_news?scope=all&amp;start_date=2026-03-26&amp;end_date=2026-03-27')
        self.assertContains(response, '/tushare/pro/cjzc?limit=20')
        self.assertContains(response, '/tushare/pro/cjzc?start_date=2026-03-20&amp;end_date=2026-03-27')
        self.assertContains(response, '/tushare/pro/news_cctv?date=2026-03-26&amp;limit=20')
        self.assertContains(response, '/tushare/pro/news_economic_baidu?date=2026-03-26&amp;limit=50')
        self.assertContains(response, '历史区间')
        self.assertContains(response, 'https://ai-tool.indevs.in/tushare/pro/express_news')
        self.assertContains(response, 'https://ai-tool.indevs.in/tushare/pro/cjzc')
        self.assertContains(response, 'start_date&quot;: &quot;2026-03-26&quot;')
        self.assertContains(response, 'end_date&quot;: &quot;2026-03-27&quot;')
        self.assertNotContains(response, '/tushare/pro/news?src=sina')
        self.assertNotContains(response, '/tushare/pro/major_news')

    @patch('tools.views.RELAY_HTTP_SESSION.get')
    def test_quant_tushare_catalog_marks_irm_qa_as_news_like_data(self, mock_get):
        class _CatalogResponse:
            ok = True

            @staticmethod
            def json():
                return {
                    'categories': {'互动易问答（沪深）': ['irm_qa_sh', 'irm_qa_sz']},
                    'examples': {
                        '互动易问答（沪深）': [
                            {
                                'api_name': 'irm_qa_sh',
                                'params': {'ts_code': '600000.SH'},
                                'example_url': '/pro/irm_qa_sh?ts_code=600000.SH',
                            },
                            {
                                'api_name': 'irm_qa_sz',
                                'params': {'ts_code': '000001.SZ'},
                                'example_url': '/pro/irm_qa_sz?ts_code=000001.SZ',
                            },
                        ]
                    },
                    'cache_policy': {'historical_date_queries': '通常 3 到 7 天'},
                }

        mock_get.return_value = _CatalogResponse()
        response = self.client.get('/quant/tushare-pro-catalog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '互动易问答本质上也属于事件驱动的信息披露流，可以视作新闻数据的延伸')
        self.assertContains(response, '当前缓存 12 小时，陈旧缓存 7 天内清理')

    @patch('tools.views.RELAY_HTTP_SESSION.get')
    def test_tushare_proxy_catalog_renders_html_for_browser_without_key(self, mock_get):
        class _CatalogResponse:
            ok = True

            @staticmethod
            def json():
                return {
                    'categories': {'互动易问答（沪深）': ['irm_qa_sh']},
                    'examples': {
                        '互动易问答（沪深）': [
                            {
                                'api_name': 'irm_qa_sh',
                                'params': {'ts_code': '600000.SH'},
                                'example_url': '/pro/irm_qa_sh?ts_code=600000.SH',
                            }
                        ]
                    },
                }

        mock_get.return_value = _CatalogResponse()
        response = self.client.get('/tushare/pro/catalog', HTTP_ACCEPT='text/html,application/xhtml+xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '可搜索前端目录页')
        self.assertContains(response, 'irm_qa_sh')

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_catalog_with_plain_api_key(self, mock_request):
        service = ApiRelayService.objects.create(
            slug='placeholder',
            name='Placeholder',
            base_url='http://127.0.0.1:9002',
            is_active=True,
        )
        service.delete()
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )
        key_user = User.objects.create_user(username='tushare_catalog_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 21, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey',
            api_key_secret_hash=make_password('plainkey'),
            api_key_last4='nkey',
        )

        class _FakeResponse:
            status_code = 200
            content = json.dumps({'code': 0, 'examples': {'股票': []}}).encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()
        response = self.client.get('/tushare/pro/catalog', HTTP_X_API_KEY='plainkey')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs['url'], 'http://127.0.0.1:8001/pro/catalog')

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    @patch('tools.views.timezone.localtime')
    def test_tushare_proxy_accepts_temporary_api_key_before_6pm(self, mock_localtime, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        class _FakeResponse:
            status_code = 200
            content = json.dumps({'code': 0, 'ok': True}).encode()
            headers = {'Content-Type': 'application/json'}

        mock_localtime.return_value = datetime(2026, 3, 23, 17, 59, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_request.return_value = _FakeResponse()
        response = self.client.get('/tushare/daily/news', HTTP_X_API_KEY='20260323')

        self.assertEqual(response.status_code, 200)
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs['url'], 'http://127.0.0.1:8001/daily/news')
        self.assertEqual(kwargs['headers']['X-Ai-Tools-Relay-Service'], 'tushare')
        self.assertNotIn('X-Ai-Tools-Username', kwargs['headers'])

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    @patch('tools.views.timezone.localtime')
    def test_tushare_proxy_rejects_temporary_api_key_at_or_after_6pm(self, mock_localtime, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        mock_localtime.return_value = datetime(2026, 3, 23, 18, 0, tzinfo=ZoneInfo('Asia/Shanghai'))
        response = self.client.get('/tushare/daily/news', HTTP_X_API_KEY='20260323')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'invalid_api_key')
        mock_request.assert_not_called()

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_caches_news_for_one_hour_in_database(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_news_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey',
            api_key_secret_hash=make_password('plainkey'),
            api_key_last4='nkey',
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'news', 'count': 1, 'data': [{'title': 'cached'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/news',
            {'src': 'sina', 'fields': 'title'},
            HTTP_X_API_KEY='plainkey',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(TushareNewsCache.objects.count(), 1)
        self.assertEqual(TushareNewsCache.objects.first().cache_bucket, 'news')
        self.assertEqual(mock_request.call_count, 1)

        mock_request.reset_mock()
        response = self.client.get(
            '/tushare/pro/news',
            {'src': 'sina', 'fields': 'title'},
            HTTP_X_API_KEY='plainkey',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        self.assertEqual(response.json()['count'], 1)
        mock_request.assert_not_called()

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_refreshes_news_cache_after_one_hour(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_news_refresh_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey_refresh',
            api_key_secret_hash=make_password('plainkey_refresh'),
            api_key_last4='resh',
        )

        cache_key = hashlib.sha256('pro/news?fields=title&src=sina'.encode('utf-8')).hexdigest()
        cache_entry = TushareNewsCache.objects.create(
            cache_key=cache_key,
            relay_path='pro/news',
            query_string='fields=title&src=sina',
            response_body=json.dumps({'api_name': 'news', 'count': 1, 'data': [{'title': 'stale'}]}),
            status_code=200,
            content_type='application/json',
        )
        TushareNewsCache.objects.filter(pk=cache_entry.pk).update(
            updated_at=timezone.now() - timedelta(hours=1, seconds=1)
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'news', 'count': 1, 'data': [{'title': 'fresh'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/news',
            {'src': 'sina', 'fields': 'title'},
            HTTP_X_API_KEY='plainkey_refresh',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(response.json()['data'][0]['title'], 'fresh')
        self.assertEqual(mock_request.call_count, 1)
        self.assertEqual(TushareNewsCache.objects.count(), 1)

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_caches_major_news_for_one_day_in_database(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_major_news_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='major_plainkey',
            api_key_secret_hash=make_password('major_plainkey'),
            api_key_last4='nkey',
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'major_news', 'count': 1, 'data': [{'title': 'cached major'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/major_news',
            {'src': '新浪财经', 'fields': 'title,content', 'start_date': '2026-03-26 00:00:00'},
            HTTP_X_API_KEY='major_plainkey',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(TushareNewsCache.objects.count(), 1)
        self.assertEqual(mock_request.call_count, 1)

        mock_request.reset_mock()
        response = self.client.get(
            '/tushare/pro/major_news',
            {'src': '新浪财经', 'fields': 'title,content', 'start_date': '2026-03-26 00:00:00'},
            HTTP_X_API_KEY='major_plainkey',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        self.assertEqual(response.json()['count'], 1)
        mock_request.assert_not_called()

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_refreshes_major_news_cache_after_one_day(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_major_news_refresh_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='major_refresh_key',
            api_key_secret_hash=make_password('major_refresh_key'),
            api_key_last4='resh',
        )

        cache_key = hashlib.sha256(
            'pro/major_news?fields=title%2Ccontent&src=%E6%96%B0%E6%B5%AA%E8%B4%A2%E7%BB%8F&start_date=2026-03-26+00%3A00%3A00'.encode('utf-8')
        ).hexdigest()
        cache_entry = TushareNewsCache.objects.create(
            cache_key=cache_key,
            relay_path='pro/major_news',
            query_string='fields=title%2Ccontent&src=%E6%96%B0%E6%B5%AA%E8%B4%A2%E7%BB%8F&start_date=2026-03-26+00%3A00%3A00',
            response_body=json.dumps({'api_name': 'major_news', 'count': 1, 'data': [{'title': 'stale major'}]}),
            status_code=200,
            content_type='application/json',
        )
        TushareNewsCache.objects.filter(pk=cache_entry.pk).update(
            updated_at=timezone.now() - timedelta(days=1, seconds=1)
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'major_news', 'count': 1, 'data': [{'title': 'fresh major'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/major_news',
            {'src': '新浪财经', 'fields': 'title,content', 'start_date': '2026-03-26 00:00:00'},
            HTTP_X_API_KEY='major_refresh_key',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(response.json()['data'][0]['title'], 'fresh major')
        self.assertEqual(mock_request.call_count, 1)
        self.assertEqual(TushareNewsCache.objects.count(), 1)

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_caches_irm_qa_for_twelve_hours_in_database(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_irm_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='irm_plainkey',
            api_key_secret_hash=make_password('irm_plainkey'),
            api_key_last4='nkey',
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'irm_qa_sh', 'count': 1, 'data': [{'q': 'cached irm'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/irm_qa_sh',
            {'ts_code': '600000.SH', 'fields': 'ts_code,q,a,pub_time'},
            HTTP_X_API_KEY='irm_plainkey',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(TushareNewsCache.objects.count(), 1)
        self.assertEqual(mock_request.call_count, 1)

        mock_request.reset_mock()
        response = self.client.get(
            '/tushare/pro/irm_qa_sh',
            {'ts_code': '600000.SH', 'fields': 'ts_code,q,a,pub_time'},
            HTTP_X_API_KEY='irm_plainkey',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        mock_request.assert_not_called()

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_refreshes_irm_qa_cache_after_twelve_hours(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_irm_refresh_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='irm_refresh_key',
            api_key_secret_hash=make_password('irm_refresh_key'),
            api_key_last4='resh',
        )

        cache_key = hashlib.sha256('pro/irm_qa_sh?fields=ts_code%2Cq%2Ca%2Cpub_time&ts_code=600000.SH'.encode('utf-8')).hexdigest()
        cache_entry = TushareNewsCache.objects.create(
            cache_key=cache_key,
            relay_path='pro/irm_qa_sh',
            query_string='fields=ts_code%2Cq%2Ca%2Cpub_time&ts_code=600000.SH',
            response_body=json.dumps({'api_name': 'irm_qa_sh', 'count': 1, 'data': [{'q': 'stale irm'}]}),
            status_code=200,
            content_type='application/json',
        )
        TushareNewsCache.objects.filter(pk=cache_entry.pk).update(
            updated_at=timezone.now() - timedelta(hours=12, seconds=1)
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'irm_qa_sh', 'count': 1, 'data': [{'q': 'fresh irm'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/irm_qa_sh',
            {'ts_code': '600000.SH', 'fields': 'ts_code,q,a,pub_time'},
            HTTP_X_API_KEY='irm_refresh_key',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(response.json()['data'][0]['q'], 'fresh irm')
        self.assertEqual(mock_request.call_count, 1)

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_purges_old_irm_qa_cache_entries(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_irm_purge_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='irm_purge_key',
            api_key_secret_hash=make_password('irm_purge_key'),
            api_key_last4='urge',
        )

        old_entry = TushareNewsCache.objects.create(
            cache_key='a' * 64,
            relay_path='pro/irm_qa_sh',
            query_string='ts_code=600000.SH',
            response_body=json.dumps({'api_name': 'irm_qa_sh', 'count': 1, 'data': [{'q': 'ancient irm'}]}),
            status_code=200,
            content_type='application/json',
        )
        TushareNewsCache.objects.filter(pk=old_entry.pk).update(
            updated_at=timezone.now() - timedelta(days=7, seconds=1)
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'irm_qa_sh', 'count': 1, 'data': [{'q': 'new irm'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/irm_qa_sh',
            {'ts_code': '600001.SH'},
            HTTP_X_API_KEY='irm_purge_key',
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TushareNewsCache.objects.filter(pk=old_entry.pk).exists())

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_caches_generic_historical_pro_data(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_anns_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='anns_cache_key',
            api_key_secret_hash=make_password('anns_cache_key'),
            api_key_last4='ache',
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'anns_d', 'count': 1, 'data': [{'title': '公告一'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/anns_d',
            {'ann_date': '20260327', 'ts_code': '000001.SZ'},
            HTTP_X_API_KEY='anns_cache_key',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(TushareNewsCache.objects.count(), 1)
        cache_entry = TushareNewsCache.objects.first()
        self.assertIsNotNone(cache_entry.fresh_until)
        self.assertIsNotNone(cache_entry.purge_after)
        self.assertGreater(cache_entry.purge_after, cache_entry.fresh_until)

        mock_request.reset_mock()
        response = self.client.get(
            '/tushare/pro/anns_d',
            {'ann_date': '20260327', 'ts_code': '000001.SZ'},
            HTTP_X_API_KEY='anns_cache_key',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        mock_request.assert_not_called()

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_purges_old_generic_historical_cache_entries(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_anns_purge_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='anns_purge_key',
            api_key_secret_hash=make_password('anns_purge_key'),
            api_key_last4='urge',
        )

        old_entry = TushareNewsCache.objects.create(
            cache_key='b' * 64,
            relay_path='pro/anns_d',
            query_string='ann_date=20260320&ts_code=000001.SZ',
            response_body=json.dumps({'api_name': 'anns_d', 'count': 1, 'data': [{'title': 'old ann'}]}),
            status_code=200,
            content_type='application/json',
            purge_after=timezone.now() - timedelta(seconds=1),
        )

        class _FakeResponse:
            status_code = 200
            text = json.dumps({'api_name': 'anns_d', 'count': 1, 'data': [{'title': 'fresh ann'}]})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/anns_d',
            {'ann_date': '20260327', 'ts_code': '000001.SZ'},
            HTTP_X_API_KEY='anns_purge_key',
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TushareNewsCache.objects.filter(pk=old_entry.pk).exists())

    def test_tushare_replay_lease_claim_takes_over_expired_holder(self):
        now = timezone.now()
        TushareReplayLease.objects.create(
            cache_key='lease-key',
            relay_path='pro/news',
            query_string='src=sina',
            owner_token='stale-owner',
            lease_until=now - timedelta(seconds=1),
        )

        is_leader, owner_token = tool_views._claim_tushare_replay_lease(
            'lease-key',
            'pro/news',
            'src=sina',
            now=now,
        )

        self.assertTrue(is_leader)
        self.assertNotEqual(owner_token, 'stale-owner')
        lease = TushareReplayLease.objects.get(cache_key='lease-key')
        self.assertEqual(lease.owner_token, owner_token)
        self.assertGreater(lease.lease_until, now)

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    @patch('tools.views._wait_for_tushare_replay_cache_fill')
    @patch('tools.views._claim_tushare_replay_lease', return_value=(False, 'leader-owner'))
    def test_tushare_proxy_follower_reuses_cache_without_second_upstream(self, _mock_claim, mock_wait, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_follower_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='follower_key',
            api_key_secret_hash=make_password('follower_key'),
            api_key_last4='ower',
        )

        cache_key = hashlib.sha256('pro/news?fields=title&src=sina'.encode('utf-8')).hexdigest()
        cache_entry = TushareNewsCache.objects.create(
            cache_key=cache_key,
            relay_path='pro/news',
            query_string='fields=title&src=sina',
            response_body=json.dumps({'api_name': 'news', 'count': 1, 'data': [{'title': 'leader result'}]}),
            status_code=200,
            content_type='application/json',
            fresh_until=timezone.now() + timedelta(minutes=5),
            purge_after=timezone.now() + timedelta(days=1),
        )
        mock_wait.return_value = cache_entry

        response = self.client.get(
            '/tushare/pro/news',
            {'src': 'sina', 'fields': 'title'},
            HTTP_X_API_KEY='follower_key',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        self.assertEqual(response.json()['data'][0]['title'], 'leader result')
        mock_request.assert_not_called()

    def test_tushare_replay_cleanup_removes_expired_leases(self):
        TushareReplayLease.objects.create(
            cache_key='expired-lease',
            relay_path='pro/news',
            query_string='src=sina',
            owner_token='expired-owner',
            lease_until=timezone.now() - timedelta(seconds=1),
        )

        tool_views._maybe_cleanup_tushare_replay_cache(now=timezone.now(), force=True)

        self.assertFalse(TushareReplayLease.objects.filter(cache_key='expired-lease').exists())

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_briefly_caches_upstream_503_to_merge_retries(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_error_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='error_cache_key',
            api_key_secret_hash=make_password('error_cache_key'),
            api_key_last4='ache',
        )

        class _FakeResponse:
            status_code = 503
            text = json.dumps({'ok': False, 'error': 'relay_unavailable'})
            content = text.encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/news',
            {'src': 'sina'},
            HTTP_X_API_KEY='error_cache_key',
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(mock_request.call_count, 1)
        cache_entry = TushareNewsCache.objects.get(relay_path='pro/news')
        self.assertEqual(cache_entry.cache_bucket, 'error')

        mock_request.reset_mock()
        response = self.client.get(
            '/tushare/pro/news',
            {'src': 'sina'},
            HTTP_X_API_KEY='error_cache_key',
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        mock_request.assert_not_called()

    def test_tushare_replay_cleanup_trims_cache_bucket_capacity(self):
        news_limit = tool_views.TUSHARE_CACHE_BUCKET_LIMITS['news']
        now = timezone.now()
        for index in range(news_limit + 5):
            TushareNewsCache.objects.create(
                cache_key=f'news-{index:064d}'[-64:],
                cache_bucket='news',
                relay_path='pro/news',
                query_string=f'page={index}',
                response_body=json.dumps({'page': index}),
                status_code=200,
                content_type='application/json',
                fresh_until=now + timedelta(hours=1),
                purge_after=now + timedelta(days=1),
            )

        deleted = tool_views._trim_tushare_replay_cache_buckets()

        self.assertEqual(deleted, 5)
        self.assertEqual(TushareNewsCache.objects.filter(cache_bucket='news').count(), news_limit)

    @patch('tools.views.ak.stock_info_global_cls')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_express_news_without_upstream_request(self, mock_request, mock_cls):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_express_news_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='express_key',
            api_key_secret_hash=make_password('express_key'),
            api_key_last4='ess1',
        )

        import pandas as pd
        mock_cls.return_value = pd.DataFrame([
            {'标题': '快讯一', '内容': '内容一', '发布日期': '2026-03-27', '发布时间': '12:00:00'},
            {'标题': '快讯二', '内容': '内容二', '发布日期': '2026-03-27', '发布时间': '12:05:00'},
        ])

        response = self.client.get(
            '/tushare/pro/express_news',
            {'scope': 'all', 'limit': '1', 'fields': 'title,datetime,src'},
            HTTP_X_API_KEY='express_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'express_news')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['title'], '快讯一')
        self.assertEqual(payload['data'][0]['src'], 'express')
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        mock_request.assert_not_called()

    @patch('tools.views.TUSHARE_DIRECT_HTTP_SESSION.get')
    @patch('tools.views.ak.stock_info_global_cls')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_historical_express_news_from_cls_pages(self, mock_request, mock_cls, mock_direct_get):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_express_hist_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='express_hist_key',
            api_key_secret_hash=make_password('express_hist_key'),
            api_key_last4='hist',
        )

        page_one_oldest = int(datetime(2026, 3, 27, 0, 30, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp())

        class _FakeClsPageResponse:
            status_code = 200
            headers = {'Content-Type': 'application/json'}

            def __init__(self, rows):
                self._payload = {'error': 0, 'data': {'roll_data': rows}}
                self.text = json.dumps(self._payload, ensure_ascii=False)
                self.content = self.text.encode('utf-8')

            def json(self):
                return self._payload

            def raise_for_status(self):
                return None

        mock_direct_get.side_effect = [
            _FakeClsPageResponse([
                {
                    'id': 101,
                    'title': '非历史窗口',
                    'content': '2026-03-27',
                    'ctime': int(datetime(2026, 3, 27, 9, 0, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp()),
                    'level': 'C',
                },
                {
                    'id': 102,
                    'title': '历史快讯二',
                    'content': '命中 2026-03-26',
                    'ctime': int(datetime(2026, 3, 26, 14, 30, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp()),
                    'level': 'A',
                },
                {
                    'id': 103,
                    'title': '页尾游标',
                    'content': '用于翻页',
                    'ctime': page_one_oldest,
                    'level': 'C',
                },
            ]),
            _FakeClsPageResponse([
                {
                    'id': 103,
                    'title': '页尾游标',
                    'content': '重复项应去重',
                    'ctime': page_one_oldest,
                    'level': 'C',
                },
                {
                    'id': 104,
                    'title': '历史快讯一',
                    'content': '命中 2026-03-25',
                    'ctime': int(datetime(2026, 3, 25, 10, 15, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp()),
                    'level': 'B',
                },
                {
                    'id': 105,
                    'title': '超出窗口',
                    'content': '2026-03-24',
                    'ctime': int(datetime(2026, 3, 24, 22, 0, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp()),
                    'level': 'C',
                },
            ]),
        ]

        response = self.client.get(
            '/tushare/pro/express_news',
            {
                'scope': 'all',
                'start_date': '2026-03-25',
                'end_date': '2026-03-26',
                'fields': 'title,content,datetime,src',
            },
            HTTP_X_API_KEY='express_hist_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'express_news')
        self.assertEqual(payload['count'], 2)
        self.assertEqual(payload['data'][0]['title'], '历史快讯一')
        self.assertEqual(payload['data'][1]['title'], '历史快讯二')
        self.assertEqual(payload['data'][0]['src'], 'cls')
        self.assertEqual(
            payload['params'],
            {
                'scope': 'all',
                'start_date': '2026-03-25 00:00:00',
                'end_date': '2026-03-26 23:59:59',
                'fields': 'title,content,datetime,src',
            },
        )
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        mock_cls.assert_not_called()
        mock_request.assert_not_called()

        self.assertEqual(mock_direct_get.call_count, 2)
        first_call_params = mock_direct_get.call_args_list[0].kwargs['params']
        second_call_params = mock_direct_get.call_args_list[1].kwargs['params']
        self.assertNotIn('lastTime', first_call_params)
        self.assertEqual(
            second_call_params['last_time'],
            str(int(datetime(2026, 3, 26, 14, 30, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp())),
        )
        self.assertEqual(second_call_params['lastTime'], second_call_params['last_time'])

    @patch('tools.views.TUSHARE_DIRECT_HTTP_SESSION.get')
    @patch('tools.views.ak.stock_info_global_cls')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_passthrough_historical_express_news_when_local_source_has_no_history(self, mock_request, mock_cls, mock_direct_get):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_express_hist_fallback_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='express_hist_fallback_key',
            api_key_secret_hash=make_password('express_hist_fallback_key'),
            api_key_last4='fall',
        )

        class _FakeClsPageResponse:
            status_code = 200
            headers = {'Content-Type': 'application/json'}

            def __init__(self, rows):
                self._payload = {'error': 0, 'data': {'roll_data': rows}}
                self.text = json.dumps(self._payload, ensure_ascii=False)
                self.content = self.text.encode('utf-8')

            def json(self):
                return self._payload

            def raise_for_status(self):
                return None

        mock_direct_get.side_effect = [
            _FakeClsPageResponse([
                {
                    'id': 201,
                    'title': '仅有最新快讯',
                    'content': '2026-03-27',
                    'ctime': int(datetime(2026, 3, 27, 21, 58, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp()),
                    'level': 'B',
                },
                {
                    'id': 202,
                    'title': '仍然是最新快讯',
                    'content': '2026-03-27',
                    'ctime': int(datetime(2026, 3, 27, 21, 7, tzinfo=ZoneInfo('Asia/Shanghai')).timestamp()),
                    'level': 'B',
                },
            ]),
            _FakeClsPageResponse([]),
        ]
        class _FakeResponse:
            status_code = 200
            headers = {'Content-Type': 'application/json'}

            def __init__(self):
                self._payload = {
                    'api_name': 'express_news',
                    'code': 0,
                    'msg': 'ok',
                    'params': {
                        'scope': 'all',
                        'start_date': '2026-03-21 00:00:00',
                        'end_date': '2026-03-26 23:59:59',
                        'fields': 'title,content,datetime,src',
                    },
                    'count': 1,
                    'data': [
                        {
                            'title': '上游历史快讯',
                            'content': 'fallback',
                            'datetime': '2026-03-25 10:00:00',
                            'src': 'tushare',
                        }
                    ],
                }
                self.text = json.dumps(self._payload, ensure_ascii=False)
                self.content = self.text.encode('utf-8')

            def json(self):
                return self._payload

            def raise_for_status(self):
                return None

        mock_request.return_value = _FakeResponse()

        response = self.client.get(
            '/tushare/pro/express_news',
            {
                'scope': 'all',
                'start_date': '2026-03-21',
                'end_date': '2026-03-26',
                'fields': 'title,content,datetime,src',
            },
            HTTP_X_API_KEY='express_hist_fallback_key',
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['title'], '上游历史快讯')
        self.assertEqual(payload['data'][0]['src'], 'tushare')
        mock_cls.assert_not_called()
        mock_request.assert_called_once()

    @patch('tools.views.ak.stock_info_cjzc_em')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_cjzc_without_upstream_request(self, mock_request, mock_cjzc):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_cjzc_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='cjzc_key',
            api_key_secret_hash=make_password('cjzc_key'),
            api_key_last4='cjzc',
        )

        import pandas as pd
        mock_cjzc.return_value = pd.DataFrame([
            {'标题': '东方财富财经早餐 3月27日周五', '摘要': '摘要一', '发布时间': '2026-03-27 07:30:00', '链接': 'https://example.com/1'},
            {'标题': '东方财富财经早餐 3月26日周四', '摘要': '摘要二', '发布时间': '2026-03-26 07:30:00', '链接': 'https://example.com/2'},
        ])

        response = self.client.get(
            '/tushare/pro/cjzc',
            {'limit': '1', 'fields': 'title,pub_time,src'},
            HTTP_X_API_KEY='cjzc_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'cjzc')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['title'], '东方财富财经早餐 3月27日周五')
        self.assertEqual(payload['data'][0]['src'], 'cjzc')
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_info_cjzc_em')
    def test_tushare_proxy_serves_historical_cjzc(self, mock_cjzc):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_cjzc_hist_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='cjzc_hist',
            api_key_secret_hash=make_password('cjzc_hist'),
            api_key_last4='hist',
        )

        import pandas as pd
        mock_cjzc.return_value = pd.DataFrame([
            {'标题': '东方财富财经早餐 3月27日周五', '摘要': '摘要三', '发布时间': '2026-03-27 07:30:00', '链接': 'https://example.com/3'},
            {'标题': '东方财富财经早餐 3月26日周四', '摘要': '摘要二', '发布时间': '2026-03-26 07:30:00', '链接': 'https://example.com/2'},
            {'标题': '东方财富财经早餐 3月25日周三', '摘要': '摘要一', '发布时间': '2026-03-25 07:30:00', '链接': 'https://example.com/1'},
        ])

        response = self.client.get(
            '/tushare/pro/cjzc',
            {'start_date': '2026-03-25', 'end_date': '2026-03-26', 'fields': 'title,summary,pub_time,url'},
            HTTP_X_API_KEY='cjzc_hist',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'cjzc')
        self.assertEqual(payload['count'], 2)
        self.assertEqual(payload['data'][0]['title'], '东方财富财经早餐 3月25日周三')
        self.assertEqual(payload['data'][1]['title'], '东方财富财经早餐 3月26日周四')
        self.assertEqual(
            payload['params'],
            {
                'fields': 'title,summary,pub_time,url',
                'start_date': '2026-03-25 00:00:00',
                'end_date': '2026-03-26 23:59:59',
            },
        )

    @patch('tools.views.ak.index_global_spot_em')
    @patch('tools.views.ak.stock_hk_index_spot_em')
    @patch('tools.views.ak.stock_zh_index_spot_sina')
    @patch('tools.views.ak.index_stock_info')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_index_basic_without_upstream_request(self, mock_request, mock_index_stock_info, mock_cn_spot, mock_hk_spot, mock_global_spot):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_index_basic_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='index_basic_key',
            api_key_secret_hash=make_password('index_basic_key'),
            api_key_last4='asic',
        )

        import pandas as pd
        mock_index_stock_info.return_value = pd.DataFrame([
            {'index_code': '000001', 'display_name': '上证指数', 'publish_date': '1991-07-15'},
        ])
        mock_cn_spot.return_value = pd.DataFrame([
            {'代码': 'sh000001', '名称': '上证指数', '最新价': 3100.0},
        ])
        mock_hk_spot.return_value = pd.DataFrame(columns=['代码', '名称'])
        mock_global_spot.return_value = pd.DataFrame(columns=['代码', '名称'])

        response = self.client.get(
            '/tushare/pro/index_basic',
            {'market': 'CN', 'limit': '10'},
            HTTP_X_API_KEY='index_basic_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'index_basic')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['ts_code'], '000001.SH')
        self.assertEqual(payload['data'][0]['name'], '上证指数')
        mock_request.assert_not_called()

    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_passthrough_index_basic_for_unsupported_market(self, mock_request):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_index_basic_passthrough_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='index_basic_pass',
            api_key_secret_hash=make_password('index_basic_pass'),
            api_key_last4='pass',
        )

        class _FakeResponse:
            status_code = 200
            content = json.dumps({'code': 0, 'api_name': 'index_basic', 'data': [{'ts_code': 'SPX'}]}).encode()
            headers = {'Content-Type': 'application/json'}

        mock_request.return_value = _FakeResponse()
        response = self.client.get(
            '/tushare/pro/index_basic',
            {'market': 'MSCI'},
            HTTP_X_API_KEY='index_basic_pass',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['api_name'], 'index_basic')
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs['url'], 'http://127.0.0.1:8001/pro/index_basic')

    @patch('tools.views.ak.stock_zh_index_daily')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_index_daily_without_upstream_request(self, mock_request, mock_index_daily):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_index_daily_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='index_daily_key',
            api_key_secret_hash=make_password('index_daily_key'),
            api_key_last4='aily',
        )

        import pandas as pd
        mock_index_daily.return_value = pd.DataFrame([
            {'date': date(2026, 3, 1), 'open': 3300.0, 'high': 3320.0, 'low': 3290.0, 'close': 3310.0, 'volume': 1000000},
            {'date': date(2026, 3, 2), 'open': 3310.0, 'high': 3330.0, 'low': 3300.0, 'close': 3325.0, 'volume': 1200000},
        ])

        response = self.client.get(
            '/tushare/pro/index_daily',
            {'ts_code': '000001.SH', 'start_date': '2026-03-01', 'end_date': '2026-03-02', 'limit': '10'},
            HTTP_X_API_KEY='index_daily_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'index_daily')
        self.assertEqual(payload['count'], 2)
        self.assertEqual(payload['data'][0]['ts_code'], '000001.SH')
        self.assertEqual(payload['data'][0]['trade_date'], '20260302')
        self.assertEqual(payload['data'][1]['trade_date'], '20260301')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_zh_index_spot_sina')
    def test_tushare_proxy_serves_index_latest_without_upstream_request(self, mock_cn_spot):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_index_latest_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='index_latest_key',
            api_key_secret_hash=make_password('index_latest_key'),
            api_key_last4='test',
        )

        import pandas as pd
        mock_cn_spot.return_value = pd.DataFrame([
            {
                '代码': 'sh000001',
                '名称': '上证指数',
                '最新价': 3310.0,
                '涨跌额': 12.0,
                '涨跌幅': 0.36,
                '昨收': 3298.0,
                '今开': 3301.0,
                '最高': 3315.0,
                '最低': 3295.0,
                '成交量': 1000000,
                '成交额': 2000000,
            },
        ])

        response = self.client.get(
            '/tushare/index/000001.SH/latest',
            HTTP_X_API_KEY='index_latest_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['data']['ts_code'], '000001.SH')
        self.assertEqual(payload['data']['name'], '上证指数')
        self.assertEqual(payload['data']['path'], '/tushare/index/000001.SH/latest')

    @patch('tools.views.ak.stock_analyst_rank_em')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_analyst_rank_without_upstream_request(self, mock_request, mock_rank):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_analyst_rank_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='analyst_rank_key',
            api_key_secret_hash=make_password('analyst_rank_key'),
            api_key_last4='rank',
        )

        import pandas as pd
        mock_rank.return_value = pd.DataFrame([
            {
                '分析师名称': '任志强',
                '分析师单位': '华福证券',
                '年度指数': 6424.01,
                '12个月收益率': 135.17,
                '分析师ID': '11000213851',
                '行业': '电子',
                '更新日期': date(2024, 12, 31),
                '年度': '2024',
            },
        ])

        response = self.client.get(
            '/tushare/pro/analyst_rank',
            {'year': '2024', 'limit': '1'},
            HTTP_X_API_KEY='analyst_rank_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'analyst_rank')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['分析师名称'], '任志强')
        self.assertEqual(payload['params']['year'], '2024')
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_analyst_detail_em')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_analyst_detail_without_upstream_request(self, mock_request, mock_detail):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_analyst_detail_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='analyst_detail_key',
            api_key_secret_hash=make_password('analyst_detail_key'),
            api_key_last4='tail',
        )

        import pandas as pd
        mock_detail.return_value = pd.DataFrame([
            {
                '股票代码': '002410',
                '股票名称': '广联达',
                '调入日期': date(2025, 11, 4),
                '最新评级日期': date(2025, 11, 4),
                '当前评级名称': '增持',
                '最新价格': 11.14,
                '阶段涨跌幅': -23.44,
            },
        ])

        response = self.client.get(
            '/tushare/pro/analyst_detail',
            {'analyst_id': '11000213851', 'indicator': '最新跟踪成分股', 'limit': '1'},
            HTTP_X_API_KEY='analyst_detail_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'analyst_detail')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['股票代码'], '002410')
        self.assertEqual(payload['params']['analyst_id'], '11000213851')
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_research_report_em')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_research_report_without_upstream_request(self, mock_request, mock_report):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_research_report_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='research_report_key',
            api_key_secret_hash=make_password('research_report_key'),
            api_key_last4='port',
        )

        import pandas as pd
        mock_report.return_value = pd.DataFrame([
            {
                '股票代码': '000001',
                '股票简称': '平安银行',
                '报告名称': '年报点评',
                '东财评级': '中性',
                '机构': '国信证券',
                '日期': date(2026, 3, 22),
                '报告PDF链接': 'https://example.com/report.pdf',
            },
        ])

        response = self.client.get(
            '/tushare/pro/research_report',
            {'ts_code': '000001.SZ', 'limit': '1'},
            HTTP_X_API_KEY='research_report_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'research_report')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['股票简称'], '平安银行')
        self.assertEqual(payload['params']['symbol'], '000001')
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        mock_request.assert_not_called()

    @patch('tools.views.ak.news_cctv')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_news_cctv_without_upstream_request(self, mock_request, mock_news_cctv):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_news_cctv_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='news_cctv_key',
            api_key_secret_hash=make_password('news_cctv_key'),
            api_key_last4='cctv',
        )

        import pandas as pd
        mock_news_cctv.return_value = pd.DataFrame([
            {'date': '20260326', 'title': '新闻联播标题', 'content': '新闻联播正文'},
        ])

        response = self.client.get(
            '/tushare/pro/news_cctv',
            {'date': '2026-03-26', 'limit': '1'},
            HTTP_X_API_KEY='news_cctv_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'news_cctv')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['title'], '新闻联播标题')
        self.assertEqual(payload['params']['date'], '20260326')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_notice_report')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_stock_notice_report_without_upstream_request(self, mock_request, mock_notice):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_notice_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='notice_key',
            api_key_secret_hash=make_password('notice_key'),
            api_key_last4='tice',
        )

        import pandas as pd
        mock_notice.return_value = pd.DataFrame([
            {
                '代码': '000001',
                '名称': '平安银行',
                '公告标题': '关于年度分红的公告',
                '公告类型': '财务报告',
                '公告日期': date(2026, 3, 26),
                '网址': 'https://example.com/notice',
            },
        ])

        response = self.client.get(
            '/tushare/pro/stock_notice_report',
            {'symbol': '全部', 'date': '2026-03-26', 'limit': '1'},
            HTTP_X_API_KEY='notice_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'stock_notice_report')
        self.assertEqual(payload['data'][0]['名称'], '平安银行')
        self.assertEqual(payload['params']['date'], '20260326')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_zh_a_disclosure_report_cninfo')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_cninfo_disclosure_without_upstream_request(self, mock_request, mock_disclosure):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_cninfo_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='cninfo_key',
            api_key_secret_hash=make_password('cninfo_key'),
            api_key_last4='info',
        )

        import pandas as pd
        mock_disclosure.return_value = pd.DataFrame([
            {
                '代码': '000001',
                '简称': '平安银行',
                '公告标题': '董事会决议公告',
                '公告时间': '2026-03-26',
                '公告链接': 'http://www.cninfo.com.cn/example',
            },
        ])

        response = self.client.get(
            '/tushare/pro/stock_zh_a_disclosure_report_cninfo',
            {'symbol': '000001.SZ', 'start_date': '2026-03-20', 'end_date': '2026-03-26', 'limit': '1'},
            HTTP_X_API_KEY='cninfo_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'stock_zh_a_disclosure_report_cninfo')
        self.assertEqual(payload['data'][0]['简称'], '平安银行')
        self.assertEqual(payload['params']['symbol'], '000001')
        mock_request.assert_not_called()

    @patch('tools.views.ak.news_economic_baidu')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_baidu_economic_calendar_without_upstream_request(self, mock_request, mock_calendar):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_baidu_calendar_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='baidu_calendar',
            api_key_secret_hash=make_password('baidu_calendar'),
            api_key_last4='idar',
        )

        import pandas as pd
        mock_calendar.return_value = pd.DataFrame([
            {'日期': date(2026, 3, 26), '时间': '09:00', '地区': '中国', '事件': 'CPI', '公布': 2.1, '预期': 2.0, '前值': 1.9, '重要性': 3},
        ])

        response = self.client.get(
            '/tushare/pro/news_economic_baidu',
            {'date': '20260326', 'limit': '1'},
            HTTP_X_API_KEY='baidu_calendar',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'news_economic_baidu')
        self.assertEqual(payload['data'][0]['事件'], 'CPI')
        self.assertEqual(payload['params']['date'], '20260326')
        mock_request.assert_not_called()

    @patch('tools.views.ak.fund_announcement_report_em')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_fund_announcement_without_upstream_request(self, mock_request, mock_fund_notice):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_fund_notice_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='fund_notice_key',
            api_key_secret_hash=make_password('fund_notice_key'),
            api_key_last4='fund',
        )

        import pandas as pd
        mock_fund_notice.return_value = pd.DataFrame([
            {'基金代码': '000001', '基金名称': '华夏成长混合', '公告标题': '2025年年报', '公告日期': date(2026, 3, 26), '报告ID': 'AN123'},
        ])

        response = self.client.get(
            '/tushare/pro/fund_announcement_report_em',
            {'symbol': '000001', 'limit': '1'},
            HTTP_X_API_KEY='fund_notice_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'fund_announcement_report_em')
        self.assertEqual(payload['data'][0]['基金名称'], '华夏成长混合')
        self.assertEqual(payload['params']['symbol'], '000001')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_research_report_em')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_stock_research_report_em_alias_without_upstream_request(self, mock_request, mock_report):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_stock_research_alias_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='stock_report',
            api_key_secret_hash=make_password('stock_report'),
            api_key_last4='port',
        )

        import pandas as pd
        mock_report.return_value = pd.DataFrame([
            {'股票代码': '000001', '股票简称': '平安银行', '报告名称': '年报点评', '东财评级': '买入', '机构': '国信证券', '日期': date(2026, 3, 22), '报告PDF链接': 'https://example.com/report.pdf'},
        ])

        response = self.client.get(
            '/tushare/pro/stock_research_report_em',
            {'symbol': '000001', 'limit': '1'},
            HTTP_X_API_KEY='stock_report',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'stock_research_report_em')
        self.assertEqual(payload['data'][0]['股票简称'], '平安银行')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_analyst_detail_em')
    @patch('tools.views.RELAY_HTTP_SESSION.request')
    def test_tushare_proxy_serves_analyst_history_without_upstream_request(self, mock_request, mock_detail):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_analyst_history_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='analyst_history_key',
            api_key_secret_hash=make_password('analyst_history_key'),
            api_key_last4='stor',
        )

        import pandas as pd
        mock_detail.return_value = pd.DataFrame([
            {
                '股票代码': '688256',
                '股票名称': '寒武纪',
                '调入日期': date(2024, 5, 21),
                '调出日期': date(2024, 11, 21),
                '调入时评级名称': '买入',
                '调出原因': '到期调出',
                '累计涨跌幅': 175.04,
            },
        ])

        response = self.client.get(
            '/tushare/pro/analyst_history',
            {'analyst_id': '11000213851', 'indicator': '历史跟踪成分股', 'limit': '1'},
            HTTP_X_API_KEY='analyst_history_key',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'analyst_history')
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['data'][0]['股票代码'], '688256')
        self.assertEqual(payload['params']['indicator'], '历史跟踪成分股')
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        mock_request.assert_not_called()

    @patch('tools.views.ak.stock_analyst_detail_em')
    def test_tushare_proxy_serves_analyst_history_index_series(self, mock_detail):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_analyst_history_index_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='analyst_history_index',
            api_key_secret_hash=make_password('analyst_history_index'),
            api_key_last4='ndex',
        )

        import pandas as pd
        mock_detail.return_value = pd.DataFrame([
            {'date': date(2014, 3, 31), 'value': 1000.0},
            {'date': date(2014, 4, 30), 'value': 1012.5},
        ])

        response = self.client.get(
            '/tushare/pro/analyst_history',
            {'analyst_id': '11000213851', 'indicator': '历史指数', 'limit': '2'},
            HTTP_X_API_KEY='analyst_history_index',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['api_name'], 'analyst_history')
        self.assertEqual(payload['params']['indicator'], '历史指数')
        self.assertEqual(payload['data'][0]['date'], '2014-03-31')
        self.assertEqual(payload['data'][0]['value'], 1000.0)

    @patch('tools.views.ak.stock_analyst_rank_em')
    def test_tushare_proxy_caches_analyst_rank_for_one_day(self, mock_rank):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_analyst_rank_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='analyst_rank_cache',
            api_key_secret_hash=make_password('analyst_rank_cache'),
            api_key_last4='ache',
        )

        import pandas as pd
        mock_rank.return_value = pd.DataFrame([
            {'分析师名称': '缓存分析师', '分析师ID': '1100', '年度': '2024', '更新日期': date(2024, 12, 31)},
        ])

        response = self.client.get(
            '/tushare/pro/analyst_rank',
            {'year': '2024', 'limit': '10'},
            HTTP_X_API_KEY='analyst_rank_cache',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(mock_rank.call_count, 1)

        mock_rank.reset_mock()
        response = self.client.get(
            '/tushare/pro/analyst_rank',
            {'year': '2024', 'limit': '10'},
            HTTP_X_API_KEY='analyst_rank_cache',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        mock_rank.assert_not_called()

    @patch('tools.views.ak.stock_info_global_cls')
    def test_tushare_proxy_caches_express_news_for_fifteen_minutes(self, mock_cls):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_express_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='express_cache',
            api_key_secret_hash=make_password('express_cache'),
            api_key_last4='ache',
        )

        import pandas as pd
        mock_cls.return_value = pd.DataFrame([
            {'标题': '缓存快讯', '内容': '缓存内容', '发布日期': '2026-03-27', '发布时间': '12:00:00'},
        ])

        response = self.client.get(
            '/tushare/pro/express_news',
            {'scope': 'important', 'limit': '10'},
            HTTP_X_API_KEY='express_cache',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(mock_cls.call_count, 1)

        mock_cls.reset_mock()
        response = self.client.get(
            '/tushare/pro/express_news',
            {'scope': 'important', 'limit': '10'},
            HTTP_X_API_KEY='express_cache',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        mock_cls.assert_not_called()

    @patch('tools.views.ak.stock_info_cjzc_em')
    def test_tushare_proxy_caches_cjzc_for_twelve_hours(self, mock_cjzc):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_cjzc_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='cjzc_cache',
            api_key_secret_hash=make_password('cjzc_cache'),
            api_key_last4='ache',
        )

        import pandas as pd
        mock_cjzc.return_value = pd.DataFrame([
            {'标题': '缓存晨报', '摘要': '缓存摘要', '发布时间': '2026-03-27 07:30:00', '链接': 'https://example.com/cached'},
        ])

        response = self.client.get(
            '/tushare/pro/cjzc',
            {'limit': '10'},
            HTTP_X_API_KEY='cjzc_cache',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        self.assertEqual(mock_cjzc.call_count, 1)

        mock_cjzc.reset_mock()
        response = self.client.get(
            '/tushare/pro/cjzc',
            {'limit': '10'},
            HTTP_X_API_KEY='cjzc_cache',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        mock_cjzc.assert_not_called()

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_A_SHARE_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_supports_a_share_5min_latest(self, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_minute_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey',
            api_key_secret_hash=make_password('plainkey'),
            api_key_last4='nkey',
        )

        class _FakeResponse:
            text = '=([{"day":"2026-03-23 14:25:00","open":"10.510","high":"10.520","low":"10.480","close":"10.470","volume":"12345","amount":"129345.60"}]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 23, 14, 26, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/000001.SZ/latest?freq=5MIN', HTTP_X_API_KEY='plainkey')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertEqual(payload['data']['record']['ts_code'], '000001.SZ')
        self.assertEqual(payload['data']['record']['freq'], '5MIN')
        self.assertEqual(payload['data']['record']['close'], 10.47)
        self.assertEqual(payload['data']['record']['volume'], 12345)
        self.assertEqual(payload['data']['bar_semantic'], 'latest_completed')
        self.assertTrue(payload['data']['is_complete'])
        self.assertEqual(payload['data']['period_start'], '2026-03-23 14:20:00')
        self.assertEqual(payload['data']['period_end'], '2026-03-23 14:25:00')
        self.assertEqual(response['X-Tushare-Relay-Mode'], 'a-share-5min-latest-completed')
        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args.kwargs['params'], {'symbol': 'sz000001', 'scale': '5', 'ma': 'no', 'datalen': '1970'})

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_A_SHARE_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_caches_a_share_minute_latest_until_next_bar(self, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_minute_cache_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='minute_cache_key',
            api_key_secret_hash=make_password('minute_cache_key'),
            api_key_last4='ache',
        )

        class _FakeResponse:
            text = '=([{"day":"2026-03-23 14:25:00","open":"10.510","high":"10.520","low":"10.480","close":"10.470","volume":"12345","amount":"129345.60"}]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 23, 14, 26, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/000001.SZ/latest?freq=5MIN', HTTP_X_API_KEY='minute_cache_key')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'MISS')
        cache_entry = TushareNewsCache.objects.get(relay_path='minute/000001.SZ/latest')
        self.assertEqual(cache_entry.cache_bucket, 'minute_latest')
        self.assertIsNotNone(cache_entry.fresh_until)
        self.assertIsNotNone(cache_entry.purge_after)

        mock_get.reset_mock()
        response = self.client.get('/tushare/minute/000001.SZ/latest?freq=5MIN', HTTP_X_API_KEY='minute_cache_key')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Api-Relay-Cache'], 'HIT')
        mock_get.assert_not_called()

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_A_SHARE_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_rejects_incomplete_current_30min_bar(self, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_minute_incomplete_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey3',
            api_key_secret_hash=make_password('plainkey3'),
            api_key_last4='key3',
        )

        class _FakeResponse:
            text = '=([{"day":"2026-03-23 10:00:00","open":"10.510","high":"10.520","low":"10.480","close":"10.470","volume":"12345","amount":"129345.60"}]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 23, 9, 35, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/000001.SZ/latest?freq=30MIN', HTTP_X_API_KEY='plainkey3')

        self.assertEqual(response.status_code, 503)
        payload = response.json()
        self.assertEqual(payload['code'], 503)
        self.assertEqual(payload['data']['bar_semantic'], 'latest_completed')
        self.assertFalse(payload['data']['is_complete'])
        self.assertEqual(payload['data']['period_end'], '2026-03-23 10:00:00')
        self.assertEqual(response['X-Tushare-Relay-Mode'], 'a-share-30min-latest-completed')

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_A_SHARE_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_supports_a_share_60min_latest(self, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_minute_60_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey60',
            api_key_secret_hash=make_password('plainkey60'),
            api_key_last4='ey60',
        )

        class _FakeResponse:
            text = '=([{"day":"2026-03-23 15:00:00","open":"10.510","high":"10.620","low":"10.480","close":"10.570","volume":"22345","amount":"229345.60"}]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 23, 15, 1, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/000001.SZ/latest?freq=60MIN', HTTP_X_API_KEY='plainkey60')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertEqual(payload['data']['record']['freq'], '60MIN')
        self.assertEqual(payload['data']['period_start'], '2026-03-23 14:00:00')
        self.assertEqual(payload['data']['period_end'], '2026-03-23 15:00:00')
        self.assertEqual(response['X-Tushare-Relay-Mode'], 'a-share-60min-latest-completed')

    @patch('tools.views.TUSHARE_A_SHARE_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_rejects_non_a_share_minute_request(self, mock_get):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_minute_invalid_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey2',
            api_key_secret_hash=make_password('plainkey2'),
            api_key_last4='key2',
        )

        response = self.client.get('/tushare/minute/CU2605.XYZ/latest?freq=30MIN', HTTP_X_API_KEY='plainkey2')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'symbol_not_supported')
        mock_get.assert_not_called()

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_FUTURES_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_supports_futures_minute_latest(self, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_futures_minute_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey4',
            api_key_secret_hash=make_password('plainkey4'),
            api_key_last4='key4',
        )

        class _FakeResponse:
            text = '=([["2026-03-26 10:10:00","3210","3215","3208","3212","456","789"],["2026-03-26 10:15:00","3212","3218","3211","3216","654","800"]]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 26, 10, 16, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/RB0/latest?freq=5MIN', HTTP_X_API_KEY='plainkey4')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertEqual(payload['data']['record']['symbol'], 'RB0')
        self.assertEqual(payload['data']['record']['freq'], '5MIN')
        self.assertEqual(payload['data']['record']['close'], 3216.0)
        self.assertEqual(payload['data']['record']['volume'], 654)
        self.assertEqual(payload['data']['bar_semantic'], 'latest_completed')
        self.assertTrue(payload['data']['is_complete'])
        self.assertEqual(payload['data']['period_start'], '2026-03-26 10:10:00')
        self.assertEqual(payload['data']['period_end'], '2026-03-26 10:15:00')
        self.assertEqual(payload['data']['path'], '/tushare/minute/RB0/latest?freq=5MIN')
        self.assertEqual(response['X-Tushare-Relay-Mode'], 'futures-5min-latest-completed')
        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args.kwargs['params'], {'symbol': 'RB0', 'type': '5'})

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_FUTURES_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_supports_futures_minute_latest_from_dict_payload(self, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_futures_minute_dict_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey7',
            api_key_secret_hash=make_password('plainkey7'),
            api_key_last4='key7',
        )

        class _FakeResponse:
            text = '=([{"d":"2026-03-26 10:14:00","o":"3212","h":"3218","l":"3211","c":"3216","v":"654","p":"800"},{"d":"2026-03-26 10:15:00","o":"3216","h":"3220","l":"3215","c":"3219","v":"700","p":"801"}]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 26, 10, 16, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/RB0/latest?freq=1MIN', HTTP_X_API_KEY='plainkey7')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertEqual(payload['data']['record']['symbol'], 'RB0')
        self.assertEqual(payload['data']['record']['freq'], '1MIN')
        self.assertEqual(payload['data']['record']['close'], 3219.0)
        self.assertEqual(payload['data']['record']['volume'], 700)
        self.assertEqual(payload['data']['period_start'], '2026-03-26 10:14:00')
        self.assertEqual(payload['data']['period_end'], '2026-03-26 10:15:00')

    @patch('tools.views.TUSHARE_FUTURES_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_rejects_unsupported_futures_freq(self, mock_get):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_futures_minute_invalid_freq_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey5',
            api_key_secret_hash=make_password('plainkey5'),
            api_key_last4='key5',
        )

        response = self.client.get('/tushare/minute/RB0/latest?freq=60MIN', HTTP_X_API_KEY='plainkey5')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'freq_not_supported')
        mock_get.assert_not_called()

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_FUTURES_MIN_HTTP_SESSION.get')
    def test_tushare_proxy_supports_specific_futures_contract_with_exchange_suffix(self, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_futures_contract_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey6',
            api_key_secret_hash=make_password('plainkey6'),
            api_key_last4='key6',
        )

        class _FakeResponse:
            text = '=([["2026-03-26 10:10:00","81230","81300","81180","81280","123","456"],["2026-03-26 10:15:00","81280","81320","81260","81310","234","460"]]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 26, 10, 16, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/CU2605.SHFE/latest?freq=5MIN', HTTP_X_API_KEY='plainkey6')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertEqual(payload['data']['record']['symbol'], 'CU2605.SHFE')
        self.assertEqual(payload['data']['record']['freq'], '5MIN')
        self.assertEqual(payload['data']['period_start'], '2026-03-26 10:10:00')
        self.assertEqual(payload['data']['period_end'], '2026-03-26 10:15:00')
        self.assertEqual(payload['data']['path'], '/tushare/minute/CU2605.SHFE/latest?freq=5MIN')
        self.assertEqual(mock_get.call_args.kwargs['params'], {'symbol': 'CU2605', 'type': '5'})

    @patch('tools.views.timezone.localtime')
    @patch('tools.views.TUSHARE_FUTURES_MIN_HTTP_SESSION.get')
    @patch('tools.views._get_futures_minute_aliases', return_value={'RB': 'RB0', 'RB0': 'RB0'})
    def test_tushare_proxy_supports_futures_product_code_alias(self, mock_aliases, mock_get, mock_localtime):
        service = ApiRelayService.objects.filter(slug='tushare').first()
        if service is None:
            service = ApiRelayService.objects.create(
                slug='tushare',
                name='Tushare Relay',
                base_url='http://127.0.0.1:8001',
                is_active=True,
                require_api_key=True,
                require_login=False,
                require_manual_approval=True,
                allowed_methods='GET,POST',
                timeout_seconds=30,
                public_path='/tushare/',
            )

        key_user = User.objects.create_user(username='tushare_futures_product_alias_key')
        UserApiRelayAccess.objects.create(
            user=key_user,
            service=service,
            is_enabled=True,
            approved_at=datetime(2026, 3, 23, 12, 0, tzinfo=ZoneInfo('UTC')),
            api_key_prefix='plainkey8',
            api_key_secret_hash=make_password('plainkey8'),
            api_key_last4='key8',
        )

        class _FakeResponse:
            text = '=([{"d":"2026-03-26 10:15:00","o":"3216","h":"3220","l":"3215","c":"3219","v":"700","p":"801"}]);'

            def raise_for_status(self):
                return None

        mock_localtime.return_value = datetime(2026, 3, 26, 10, 16, tzinfo=ZoneInfo('Asia/Shanghai'))
        mock_get.return_value = _FakeResponse()

        response = self.client.get('/tushare/minute/RB/latest?freq=1MIN', HTTP_X_API_KEY='plainkey8')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertEqual(payload['data']['record']['symbol'], 'RB')
        self.assertEqual(payload['data']['record']['freq'], '1MIN')
        self.assertEqual(mock_get.call_args.kwargs['params'], {'symbol': 'RB0', 'type': '1'})


class TardisRagTests(TestCase):
    def test_tardis_rag_returns_pricing_answer(self):
        response = self.client.post(
            '/quant/tardis-data-guide/rag/',
            data='{"question":"整月租用高档 API 多少钱？"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['ok'])
        self.assertIn('1500 元每月', payload['answer'])

    def test_tardis_rag_rejects_invalid_json(self):
        response = self.client.post(
            '/quant/tardis-data-guide/rag/',
            data='{bad json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'invalid_json')

    def test_tardis_superadmin_can_login_and_save_entry(self):
        page_response = self.client.get('/quant/tardis-data-guide/')
        self.assertEqual(page_response.status_code, 200)

        login_response = self.client.post(
            '/quant/tardis-data-guide/admin/login/',
            data={'username': 'zhanyuting', 'password': 'zhanyuting'},
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_response.json()['ok'])

        save_response = self.client.post(
            '/quant/tardis-data-guide/admin/entries/save/',
            data='{"title":"妹宝历史答复","question_hint":"妹宝 包月","keywords":"妹宝,包月,专属","answer":"妹宝专属说明：包月还是 1500 元，但可以直接把历史问答复制给客服。","sort_order":5,"is_active":true}',
            content_type='application/json',
        )
        self.assertEqual(save_response.status_code, 200)
        self.assertTrue(save_response.json()['ok'])
        self.assertEqual(TardisRagEntry.objects.count(), 1)

        rag_response = self.client.post(
            '/quant/tardis-data-guide/rag/',
            data='{"question":"妹宝包月怎么问？"}',
            content_type='application/json',
        )
        self.assertEqual(rag_response.status_code, 200)
        self.assertIn('可以直接把历史问答复制给客服', rag_response.json()['answer'])

    def test_tardis_rag_matches_equivalent_delivery_questions(self):
        TardisRagEntry.objects.create(
            title='发货形式说明',
            question_hint='发货形式,交付方式,怎么发给我',
            keywords='发货,交付,链接,发送',
            answer='数据通常通过定制链接或整理后的交付方式发给你，具体按你购买的档位来定。',
            sort_order=1,
            is_active=True,
        )
        response = self.client.post(
            '/quant/tardis-data-guide/rag/',
            data='{"question":"数据你怎么发给我呢？"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('定制链接', response.json()['answer'])

    def test_tardis_superadmin_can_extract_multiple_entries_from_bulk_text(self):
        self.client.post(
            '/quant/tardis-data-guide/admin/login/',
            data={'username': 'zhanyuting', 'password': 'zhanyuting'},
        )
        save_response = self.client.post(
            '/quant/tardis-data-guide/admin/entries/save/',
            data=json.dumps(
                {
                    'source_text': (
                        '包月的话目前是 1500 元每月，适合大量历史数据需求或团队型下载。\n\n'
                        '数据一般通过定制链接或者整理好的交付方式发给你，按购买档位来安排。\n\n'
                        '需要的话直接加微信 15180066256。'
                    ),
                    'keywords': '妹宝,历史答复',
                    'sort_order': 10,
                }
            ),
            content_type='application/json',
        )
        self.assertEqual(save_response.status_code, 200)
        payload = save_response.json()
        self.assertTrue(payload['ok'])
        self.assertGreaterEqual(payload['created_count'], 3)

        rag_response = self.client.post(
            '/quant/tardis-data-guide/rag/',
            data='{"question":"数据你怎么发给我呢？"}',
            content_type='application/json',
        )
        self.assertEqual(rag_response.status_code, 200)
        self.assertIn('定制链接', rag_response.json()['answer'])

    def test_extract_tardis_entries_from_text_supports_explicit_qa(self):
        entries = extract_tardis_entries_from_text(
            '问：发货形式是什么？\n答：一般通过链接发你。\n\n问：包月多少钱？\n答：1500 元每月。'
        )
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]['title'], '发货形式是什么？')
        self.assertIn('1500', entries[1]['answer'])

    def test_extract_tardis_entries_from_plain_paragraph_creates_multiple_topics(self):
        entries = extract_tardis_entries_from_text(
            '包月的话目前是1500元每月。数据一般通过定制链接发给你。需要的话直接加微信15180066256。'
        )
        self.assertGreaterEqual(len(entries), 3)

    def test_extract_tardis_entries_from_bullets_and_mixed_clauses(self):
        entries = extract_tardis_entries_from_text(
            '- 包月 1500 元每月，适合大量历史数据需求；数据一般通过定制链接发你。\n'
            '- 需要的话直接加微信 15180066256。'
        )
        answers = [item['answer'] for item in entries]
        self.assertTrue(any('1500' in item for item in answers))
        self.assertTrue(any('定制链接' in item for item in answers))
        self.assertTrue(any('15180066256' in item for item in answers))


class TushareRagTests(TestCase):
    def test_tushare_page_renders_rag_shell(self):
        response = self.client.get('/quant/tushare-pro-guide/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '在线客服 · 页面内 RAG')
        self.assertContains(response, 'Tushare 客服语料')
        self.assertContains(response, 'https://ai-tool.indevs.in/tushare/minute/RB0/latest')
        self.assertContains(response, 'print(response.json())')

    def test_tushare_superadmin_can_login_and_save_entry(self):
        self.client.get('/quant/tushare-pro-guide/')
        login_response = self.client.post(
            '/quant/tushare-pro-guide/admin/login/',
            data={'username': 'zhanyuting', 'password': 'zhanyuting'},
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_response.json()['ok'])

        save_response = self.client.post(
            '/quant/tushare-pro-guide/admin/entries/save/',
            data=json.dumps(
                {
                    'source_text': (
                        'Tushare 现在只支持 API Key，不再支持网页登录拿权限。'
                        ' 站内 replay 的分钟线入口支持 A股 1MIN、5MIN、15MIN、30MIN、60MIN latest，期货连续/主力支持 1MIN、5MIN、15MIN、30MIN latest。'
                        ' 如果要目录可以看 /tushare/pro/catalog。'
                    ),
                    'keywords': '权限,分钟,目录',
                    'sort_order': 10,
                }
            ),
            content_type='application/json',
        )
        self.assertEqual(save_response.status_code, 200)
        payload = save_response.json()
        self.assertTrue(payload['ok'])
        self.assertGreaterEqual(payload['created_count'], 3)
        self.assertEqual(TushareRagEntry.objects.count(), payload['created_count'])

        rag_response = self.client.post(
            '/quant/tushare-pro-guide/rag/',
            data='{"question":"分钟数据能不能通过站内接口拿？"}',
            content_type='application/json',
        )
        self.assertEqual(rag_response.status_code, 200)
        self.assertIn('30MIN', rag_response.json()['answer'])

    def test_tushare_extract_entries_from_plain_paragraph_creates_multiple_topics(self):
        entries = extract_tushare_entries_from_text(
            'Tushare 现在只支持 API Key。站内 replay 支持 A股 1MIN、5MIN、15MIN、30MIN、60MIN latest，也支持期货连续或主力符号 1MIN、5MIN、15MIN、30MIN latest。目录可以看 /tushare/pro/catalog。'
        )
        self.assertGreaterEqual(len(entries), 3)

    def test_tushare_extract_entries_from_bullets_and_mixed_clauses(self):
        entries = extract_tushare_entries_from_text(
            '- 现在只支持 API Key，不再支持网页登录拿权限。\n'
            '- 站内 replay 支持 A股 1MIN、5MIN、15MIN、30MIN、60MIN latest，目录可以看 /tushare/pro/catalog。\n'
            '- 如闲鱼链接失效，可联系微信 dreamsjtuai。'
        )
        answers = [item['answer'] for item in entries]
        self.assertTrue(any('API Key' in item for item in answers))
        self.assertTrue(any('/tushare/pro/catalog' in item for item in answers))
        self.assertTrue(any('dreamsjtuai' in item for item in answers))

    def test_tushare_rag_answers_a_share_and_futures_minutes(self):
        response = self.client.post(
            '/quant/tushare-pro-guide/rag/',
            data='{"question":"我想要A股60分钟和内盘期货5分钟，replay支持吗？"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        answer = response.json()['answer']
        self.assertIn('60MIN', answer)
        self.assertIn('5MIN', answer)

    def test_tushare_rag_answers_board_data_but_not_ths_board(self):
        response = self.client.post(
            '/quant/tushare-pro-guide/rag/',
            data='{"question":"板块数据支持吗？如果是同花顺板块呢？"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        answer = response.json()['answer']
        self.assertIn('concept', answer)
        self.assertIn('同花顺', answer)

    def test_tushare_rag_answers_replay_token_priority(self):
        response = self.client.post(
            '/quant/tushare-pro-guide/rag/',
            data='{"question":"所有 replay 现在优先用哪个 token？出问题怎么补救？"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        answer = response.json()['answer']
        self.assertIn('aa5388', answer)
        self.assertIn('009c49', answer)

    def test_tushare_rag_answers_catalog_new_categories(self):
        response = self.client.post(
            '/quant/tushare-pro-guide/rag/',
            data='{"question":"目录新增了哪些分类？公告、主连映射、交易日历这些现在有吗？"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        answer = response.json()['answer']
        self.assertIn('anns_d', answer)
        self.assertIn('fut_mapping', answer)
        self.assertIn('交易日历', answer)


class SocialRadarTests(TestCase):
    def test_social_radar_requires_login_for_submit(self):
        response = self.client.post('/social-radar/tasks/submit/', data={'task_type': 'keyword', 'keyword': 'AI Agent'})
        self.assertEqual(response.status_code, 302)

    def test_social_radar_page_renders_and_authenticated_user_can_submit(self):
        user = User.objects.create_user(username='radaruser', email='radar@example.com', password='secret123')
        page_response = self.client.get('/social-radar/')
        self.assertEqual(page_response.status_code, 200)
        self.assertContains(page_response, 'Social Radar 站内版')

        self.client.force_login(user)
        submit_response = self.client.post(
            '/social-radar/tasks/submit/',
            data={
                'task_type': 'keyword',
                'keyword': 'AI Agent',
                'state': 'auth_state_cookie.json',
                'headless': '1',
                'hydrate_fulltext': '1',
            },
        )
        self.assertEqual(submit_response.status_code, 200)
        payload = submit_response.json()
        self.assertTrue(payload['ok'])
        task = SocialRadarTask.objects.get()
        self.assertEqual(task.user, user)
        self.assertEqual(task.task_type, SocialRadarTask.TaskType.KEYWORD)
        self.assertEqual(task.status, SocialRadarTask.Status.QUEUED)

    def test_social_radar_x_task_accepts_cookie_without_state_file(self):
        user = User.objects.create_user(username='radarcookie', email='cookie@example.com', password='secret123')
        self.client.force_login(user)
        response = self.client.post(
            '/social-radar/tasks/submit/',
            data={
                'task_type': 'keyword',
                'keyword': 'AI Agent',
                'x_cookie': 'auth_token=testtoken; ct0=testct0',
                'headless': '1',
                'hydrate_fulltext': '1',
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['ok'])
        task = SocialRadarTask.objects.get(user=user)
        self.assertEqual(task.params.get('x_cookie'), 'auth_token=testtoken; ct0=testct0')

    def test_social_radar_cleanup_removes_expired_result_dir(self):
        user = User.objects.create_user(username='radarclean', email='clean@example.com', password='secret123')
        task = SocialRadarTask.objects.create(
            user=user,
            task_type=SocialRadarTask.TaskType.KEYWORD,
            status=SocialRadarTask.Status.DONE,
            stage='已完成',
            progress=100,
            storage_root='/tmp/social_radar_test_cleanup',
            result_relpath='run_a',
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        root = Path(task.storage_root)
        run_dir = root / 'run_a'
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / 'article.html').write_text('<html></html>', encoding='utf-8')

        cleaned = cleanup_expired_social_radar_results()
        task.refresh_from_db()

        self.assertEqual(cleaned, 1)
        self.assertFalse(root.exists())
        self.assertEqual(task.status, SocialRadarTask.Status.EXPIRED)
        self.assertEqual(task.storage_root, '')


class TTSRegenerateTests(TestCase):
    def test_tts_studio_recent_orders_use_generating_copy_for_queued_order(self):
        user = User.objects.create_user(username='ttsrecent', email='recent@example.com', password='secret123')
        order = TTSOrder.objects.create(
            user=user,
            contact_name='ttsrecent',
            email='recent@example.com',
            source_text='这是列表页显示测试文本',
            voice_preset=TTSOrder.VoicePreset.SERENA,
            style_notes='保持自然',
            business_usage=False,
            delivery_format=TTSOrder.DeliveryFormat.MP3,
            estimated_price='0.00',
            final_price='0.00',
            payment_status=TTSOrder.PaymentStatus.PAID,
            status=TTSOrder.Status.QUEUED,
            payment_reference='CREDIT-RECENT',
            paid_at=datetime(2026, 3, 23, 8, 0, tzinfo=ZoneInfo('UTC')),
            payment_verified_at=datetime(2026, 3, 23, 8, 0, tzinfo=ZoneInfo('UTC')),
        )

        self.client.force_login(user)
        response = self.client.get('/tts-studio/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_no)
        self.assertContains(response, '生成中')
        self.assertNotContains(response, '待生成')

    def test_order_status_uses_generating_copy_for_queued_order(self):
        order = TTSOrder.objects.create(
            contact_name='ttsuser',
            email='tts@example.com',
            source_text='这是待生成的文本',
            voice_preset=TTSOrder.VoicePreset.SERENA,
            style_notes='保持自然',
            business_usage=False,
            delivery_format=TTSOrder.DeliveryFormat.MP3,
            estimated_price='0.00',
            final_price='0.00',
            payment_status=TTSOrder.PaymentStatus.PAID,
            status=TTSOrder.Status.QUEUED,
            payment_reference='CREDIT-QUEUED',
            paid_at=datetime(2026, 3, 23, 8, 0, tzinfo=ZoneInfo('UTC')),
            payment_verified_at=datetime(2026, 3, 23, 8, 0, tzinfo=ZoneInfo('UTC')),
        )

        response = self.client.get(f'/tts-studio/status/{order.order_no}/', {'email': 'tts@example.com'})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['status'], TTSOrder.Status.QUEUED)
        self.assertEqual(payload['status_display'], '生成中')
        self.assertEqual(payload['progress_message'], '生成中')

    def test_regenerate_creates_new_order_for_delivered_order(self):
        user = User.objects.create_user(username='ttsuser', email='tts@example.com', password='secret123')
        TTSCreditAccount.objects.create(
            user=user,
            is_unlimited=False,
            char_balance=1000,
            total_purchased_chars=1000,
            total_used_chars=100,
        )
        original_order = TTSOrder.objects.create(
            user=user,
            contact_name='ttsuser',
            email='tts@example.com',
            source_text='这是需要重新生成的文本',
            voice_preset=TTSOrder.VoicePreset.SERENA,
            style_notes='保持自然',
            business_usage=True,
            delivery_format=TTSOrder.DeliveryFormat.MP3,
            estimated_price='0.00',
            final_price='0.00',
            payment_status=TTSOrder.PaymentStatus.PAID,
            status=TTSOrder.Status.DELIVERED,
            payment_reference='CREDIT-OLD',
            paid_at=datetime(2026, 3, 21, 12, 0, tzinfo=ZoneInfo('UTC')),
            payment_verified_at=datetime(2026, 3, 21, 12, 0, tzinfo=ZoneInfo('UTC')),
            delivered_at=datetime(2026, 3, 21, 12, 2, tzinfo=ZoneInfo('UTC')),
        )

        self.client.force_login(user)
        response = self.client.post(f'/tts-studio/regenerate/{original_order.order_no}/', {'email': 'tts@example.com'})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['ok'])
        self.assertEqual(TTSOrder.objects.count(), 2)
        new_order = TTSOrder.objects.exclude(pk=original_order.pk).get()
        self.assertEqual(new_order.status, TTSOrder.Status.QUEUED)
        self.assertEqual(new_order.source_text, original_order.source_text)
        self.assertIn(new_order.order_no, payload['redirect_url'])


class EdgeInferenceTests(TestCase):
    def test_edge_inference_hub_renders_and_accepts_request(self):
        offer = EdgeInferenceOffer.objects.create(
            slug='rtx5090-edge',
            name='RTX 5090 Edge',
            provider='local',
            gpu_name='RTX 5090',
            gpu_count=1,
            vram_gb='32.0',
            cpu_cores=24,
            ram_gb=128,
            disk_gb=2000,
            region='CN-Shanghai',
            network_up_mbps=1000,
            network_down_mbps=1000,
            billing_unit=EdgeInferenceOffer.BillingUnit.HOUR,
            price='12.50',
            min_rental_hours=1,
            stock=2,
            supported_models='vLLM, SGLang, Ollama',
            endpoint_protocols='OpenAI Compatible, SSH',
            is_active=True,
        )
        get_response = self.client.get('/edge-inference/')
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, 'RTX 5090 Edge')

        post_response = self.client.post(
            '/edge-inference/',
            data={
                'offer_id': offer.id,
                'contact_name': 'Alice',
                'email': 'alice@example.com',
                'wechat': 'alice_wechat',
                'requested_model': 'Qwen3-32B',
                'use_case': '我要一个可公网访问的边缘推理实例，用来做 API 推理服务。',
                'expected_concurrency': 8,
                'expected_hours': 24,
                'budget': '300',
            },
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(EdgeInferenceRequest.objects.count(), 1)
        req = EdgeInferenceRequest.objects.get()
        self.assertEqual(req.offer, offer)
        self.assertEqual(req.requested_model, 'Qwen3-32B')

    def test_edge_inference_request_can_issue_access_key(self):
        req = EdgeInferenceRequest.objects.create(
            contact_name='Bob',
            email='bob@example.com',
            requested_model='vLLM',
            use_case='我要一个可访问的推理入口。',
        )
        raw_key = req.issue_access_key()
        req.public_endpoint = 'https://ai-tool.indevs.in/api-relay/edge-demo/'
        req.ssh_host = 'ai-tool.indevs.in'
        req.ssh_username = 'user'
        req.save()
        self.assertTrue(raw_key.startswith('eik_'))
        self.assertTrue(req.api_key_prefix.startswith('eik_'))
        self.assertEqual(req.ssh_host, 'ai-tool.indevs.in')

    def test_edge_inference_offer_can_bind_real_api_relay_access(self):
        user = User.objects.create_user(username='edgeuser', password='pass123', email='edge@example.com')
        service = ApiRelayService.objects.create(
            slug='edge-demo',
            name='Edge Demo Relay',
            base_url='http://127.0.0.1:8999',
            is_active=True,
            require_api_key=True,
            public_path='/api-relay/edge-demo/',
        )
        offer = EdgeInferenceOffer.objects.create(
            slug='edge-offer',
            name='Edge Offer',
            provider='local',
            gpu_name='RTX 5090',
            relay_service=service,
            vram_gb='32.0',
            price='12.50',
            stock=1,
        )
        req = EdgeInferenceRequest.objects.create(
            user=user,
            offer=offer,
            contact_name='Edge User',
            email='edge@example.com',
            requested_model='Qwen',
            use_case='需要真实可调用的 relay 入口。',
        )
        access, created = UserApiRelayAccess.objects.get_or_create(user=user, service=service)
        self.assertTrue(created)
        raw_key = access.issue_api_key()
        access.is_enabled = True
        access.approved_at = timezone.now()
        access.save()

        req.apply_relay_access(access)
        req.save(update_fields=['public_endpoint', 'api_key_prefix', 'api_key_secret_hash', 'api_key_last4', 'api_key_created_at', 'updated_at'])

        self.assertTrue(raw_key.startswith('atk_'))
        self.assertEqual(req.public_endpoint, 'https://ai-tool.indevs.in/api-relay/edge-demo/')
        self.assertEqual(req.api_key_prefix, access.api_key_prefix)
        self.assertEqual(req.api_key_last4, access.api_key_last4)


class CodexBriefingTests(TestCase):
    def test_codex_briefing_page_renders(self):
        response = self.client.get('/codex-briefing/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '提交为并行任务')

    def test_codex_briefing_rejects_invalid_api_key(self):
        response = self.client.post(
            '/codex-briefing/tasks/submit/',
            data={
                'api_key': 'wrong-key',
                'source_text': '这是一段足够长的测试文本。' * 8,
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'invalid_api_key')

    @patch('tools.views.trigger_codex_briefing_worker')
    def test_codex_briefing_submit_creates_task(self, mock_trigger):
        response = self.client.post(
            '/codex-briefing/tasks/submit/',
            data={
                'api_key': 'huanghanchi',
                'source_text': '这是一段足够长的测试文本。' * 12,
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['ok'])
        task = CodexBriefingTask.objects.get()
        self.assertEqual(task.status, CodexBriefingTask.Status.QUEUED)
        self.assertEqual(task.source_char_count, len(('这是一段足够长的测试文本。' * 12).strip()))
        mock_trigger.assert_called_once()
        session = self.client.session
        self.assertTrue(session.get('codex_briefing_api_authed'))

    @patch('tools.views.trigger_codex_briefing_worker')
    def test_codex_briefing_allows_reuse_without_resubmitting_api_key(self, mock_trigger):
        session = self.client.session
        session['codex_briefing_api_authed'] = True
        session.save()
        response = self.client.post(
            '/codex-briefing/tasks/submit/',
            data={
                'api_key': '',
                'source_text': '这是一段足够长的测试文本。' * 12,
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['ok'])
        self.assertEqual(CodexBriefingTask.objects.count(), 1)

    def test_codex_briefing_tasks_json_returns_current_session_tasks(self):
        session = self.client.session
        session.save()
        CodexBriefingTask.objects.create(
            session_key=session.session_key,
            source_text='这是同一会话里的文本' * 6,
            source_char_count=60,
            status=CodexBriefingTask.Status.DONE,
            stage='已完成',
            progress=100,
            summary_title='会话内任务',
            summary_text='摘要',
            rendered_html='<section><p>ok</p></section>',
        )
        CodexBriefingTask.objects.create(
            session_key='other-session',
            source_text='这是其他会话里的文本' * 6,
            source_char_count=60,
        )

        response = self.client.get('/codex-briefing/tasks/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['ok'])
        self.assertEqual(len(payload['tasks']), 1)
        self.assertEqual(payload['tasks'][0]['summary_title'], '会话内任务')
