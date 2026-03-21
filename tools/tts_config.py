import os


def _read_positive_int(name: str, default: int) -> int:
    raw = os.getenv(name, '').strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(1, value)


def get_tts_runtime_rules() -> dict[str, int]:
    batch_chars = _read_positive_int('QWEN_TTS_MAX_BATCH_CHARS', 800)
    chunk_chars = min(_read_positive_int('QWEN_TTS_MAX_CHARS', 400), batch_chars)
    direct_max_chars = min(_read_positive_int('QWEN_TTS_DIRECT_MAX_CHARS', batch_chars), batch_chars)
    return {
        'direct_max_chars': direct_max_chars,
        'chunk_chars': chunk_chars,
        'batch_chars': batch_chars,
    }


def estimate_total_chunks(char_count: int) -> int:
    rules = get_tts_runtime_rules()
    if char_count <= rules['direct_max_chars']:
        return 1
    return max((char_count + rules['chunk_chars'] - 1) // rules['chunk_chars'], 1)
