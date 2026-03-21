import os
from unittest.mock import patch

from django.test import SimpleTestCase

from tools.tts_config import estimate_total_chunks, get_tts_runtime_rules


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
