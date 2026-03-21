from decimal import Decimal
from decimal import ROUND_UP

from .models import TTSOrder


VOICE_PRESET_CONFIG = {
    TTSOrder.VoicePreset.AIDEN: {
        'speaker': 'aiden',
        'display_name': 'Aiden',
        'summary': '阳光美式男声，中频清晰。母语：英语。',
        'instruction': '请使用 Aiden 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.DYLAN: {
        'speaker': 'dylan',
        'display_name': 'Dylan',
        'summary': '北京青年男声，音色清晰自然。母语：中文（北京话）。',
        'instruction': '请使用 Dylan 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.ERIC: {
        'speaker': 'eric',
        'display_name': 'Eric',
        'summary': '活泼的成都男声，声音略带沙哑。母语：中文（四川话）。',
        'instruction': '请使用 Eric 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.ONO_ANNA: {
        'speaker': 'ono_anna',
        'display_name': 'Ono_anna',
        'summary': '可爱的日语女声，音色轻快灵动。母语：日语。',
        'instruction': '请使用 Ono_anna 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.RYAN: {
        'speaker': 'ryan',
        'display_name': 'Ryan',
        'summary': '节奏感强的动态男声。母语：英语。',
        'instruction': '请使用 Ryan 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.SERENA: {
        'speaker': 'serena',
        'display_name': 'Serena',
        'summary': '温暖、柔和的年轻女声。母语：中文。',
        'instruction': '请使用 Serena 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.SOHEE: {
        'speaker': 'sohee',
        'display_name': 'Sohee',
        'summary': '温暖的韩语女声，情感丰富。母语：韩语。',
        'instruction': '请使用 Sohee 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.UNCLE_FU: {
        'speaker': 'uncle_fu',
        'display_name': 'Uncle_fu',
        'summary': '沉稳的男性声音，音色低沉圆润。母语：中文。',
        'instruction': '请使用 Uncle_fu 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.VIVIAN: {
        'speaker': 'vivian',
        'display_name': 'Vivian',
        'summary': '明亮、略带锋芒的年轻女声。母语：中文。',
        'instruction': '请使用 Vivian 内置音色朗读，重点保证自然、清晰、稳定，不要擅自切换到其他 speaker。',
        'selectable': True,
    },
    TTSOrder.VoicePreset.SWEET_VIVIAN: {
        'speaker': 'vivian',
        'display_name': '旧版预设：Vivian',
        'instruction': '请严格使用中文甜美、软糯、年轻、亲切、带轻微微笑感的女声来朗读，语气自然灵动，尾音自然上扬，语速中等偏慢，停顿清楚。不要生成中性、成熟、严肃或新闻播音腔。',
        'selectable': False,
    },
    TTSOrder.VoicePreset.GENTLE_SERENA: {
        'speaker': 'serena',
        'display_name': '旧版预设：Serena',
        'instruction': '请严格使用中文温柔、知性、成熟、稳定、可信赖的女声来朗读，语气从容，表达清晰，适合品牌介绍和知识内容。不要生成活泼甜妹感或过度轻快的风格。',
        'selectable': False,
    },
    TTSOrder.VoicePreset.YOUTHFUL_ONO: {
        'speaker': 'ono_anna',
        'display_name': '旧版预设：Ono_anna',
        'instruction': '请严格使用中文年轻、活力、轻快、元气感明显的女声来朗读，节奏更明快，适合短视频脚本和活动预告。不要生成温柔成熟或播音主持腔。',
        'selectable': False,
    },
    TTSOrder.VoicePreset.CUSTOM: {
        'speaker': 'vivian',
        'display_name': '旧版预设：定制风格',
        'instruction': '请用中文自然、清晰、商业可用的人声来朗读，并优先严格遵循用户额外给出的风格说明，不要擅自套用固定甜美风格。',
        'selectable': False,
    },
}

DEFAULT_RECHARGE_PACKS = [
    {'chars': 50000, 'label': '5 万字', 'price': Decimal('6.00')},
    {'chars': 100000, 'label': '10 万字', 'price': Decimal('12.00')},
]


def build_quote(char_count: int, business_usage: bool) -> tuple[Decimal, str]:
    base = (Decimal(char_count) * Decimal('1.2') / Decimal('10000')).quantize(Decimal('0.01'), rounding=ROUND_UP)
    if base < Decimal('0.01'):
        base = Decimal('0.01')

    if char_count <= 10000:
        tier = '万字内'
    elif char_count <= 50000:
        tier = '中长文'
    else:
        tier = '超长文'

    if business_usage:
        tier = f'{tier}商用单'
    else:
        tier = f'{tier}非商用单'

    return base, tier


def build_recharge_amount(char_amount: int) -> Decimal:
    amount = (Decimal(char_amount) * Decimal('1.2') / Decimal('10000')).quantize(Decimal('0.01'), rounding=ROUND_UP)
    if amount < Decimal('0.01'):
        amount = Decimal('0.01')
    return amount


def build_turnaround(char_count: int) -> str:
    if char_count <= 10000:
        return '付款后 2 小时内交付'
    if char_count <= 50000:
        return '付款后 6 小时内交付'
    return '付款后 12-24 小时内分批交付'


def get_voice_preset_config(preset: str, style_notes: str = '') -> dict[str, str]:
    config = dict(VOICE_PRESET_CONFIG.get(preset, VOICE_PRESET_CONFIG[TTSOrder.VoicePreset.SERENA]))
    strict_clause = (
        '必须严格按照用户当前选择的音色方案生成，不要擅自偏向甜美、温柔或其他默认风格。'
        '遇到公式、链接、Markdown 标记、特殊符号或异常字符时，优先稳定、自然、口语化处理，'
        '不要逐字符乱读，不要凭空补充原文没有的内容。'
        '如果文本中已经被预处理成“这里有一段公式内容”“这里有一段代码内容”“这里有一段表格内容”，'
        '就只读这些固定中文提示，然后立刻继续后续正常文本，不要继续自由发挥或扩写。'
    )
    if preset == TTSOrder.VoicePreset.CUSTOM and style_notes.strip():
        config['instruction'] = f"{strict_clause} {config['instruction']} 额外要求：{style_notes.strip()}"
    elif style_notes.strip():
        config['instruction'] = f"{strict_clause} {config['instruction']} 额外要求：{style_notes.strip()}"
    else:
        config['instruction'] = f"{strict_clause} {config['instruction']}"
    return config
