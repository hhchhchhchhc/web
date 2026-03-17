from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<key>[a-zA-Z0-9\-]{8,128})\.txt$', views.indexnow_key_txt, name='indexnow_key_txt'),
    path('', views.home, name='home'),
    path('free/search/', views.free_resources, name='free_resources'),
    path('tts-studio/', views.tts_studio, name='tts_studio'),
    path('tts-studio/logout/', views.tts_logout, name='tts_logout'),
    path('tts-studio/recharge/<str:order_no>/', views.tts_recharge_checkout, name='tts_recharge_checkout'),
    path('tts-studio/recharge/<str:order_no>/status/', views.tts_recharge_status, name='tts_recharge_status'),
    path('tts-studio/query/', views.tts_order_query, name='tts_order_query'),
    path('tts-studio/submitted/<str:order_no>/', views.tts_order_submitted, name='tts_order_submitted'),
    path('tts-studio/status/<str:order_no>/', views.tts_order_status, name='tts_order_status'),
    path('tts-studio/cancel/<str:order_no>/', views.tts_cancel_order, name='tts_cancel_order'),
    path('tts-studio/upload-proof/<str:order_no>/', views.tts_upload_payment_proof, name='tts_upload_payment_proof'),
    path('tts-studio/payment/webhook/<str:provider>/', views.tts_payment_webhook, name='tts_payment_webhook'),
    path('openclaw/', views.openclaw_column, name='openclaw_column'),
    path('algorithm-geek/', views.algorithm_geek_column, name='algorithm_geek_column'),
    path('psychology/', views.psychology_column, name='psychology_column'),
    path('quant/', views.quant_column, name='quant_column'),
    path(
        'psychology/evolution-not-willpower/',
        views.psychology_article_evolution,
        name='psychology_article_evolution'
    ),
    path('psychology/sleep/', views.psychology_sleep_category, name='psychology_sleep_category'),
    path(
        'psychology/sleep-anxiety-guide/',
        views.psychology_article_sleep,
        name='psychology_article_sleep'
    ),
    path(
        'psychology/zebra-stress-guide/',
        views.psychology_article_zebra_stress,
        name='psychology_article_zebra_stress'
    ),
    path(
        'quant/tardis-data-guide/',
        views.quant_article_tardis,
        name='quant_article_tardis'
    ),
    path(
        'quant/tushare-pro-guide/',
        views.quant_article_tushare,
        name='quant_article_tushare'
    ),
    path(
        'side-hustle/japan-goods-presale/',
        views.side_hustle_japan_goods,
        name='side_hustle_japan_goods'
    ),
    path(
        'side-hustle/xiaohongshu-virtual-store-matrix/',
        views.side_hustle_xiaohongshu_virtual_store_matrix,
        name='side_hustle_xiaohongshu_virtual_store_matrix'
    ),
    path(
        'guides/nano-banana-pro/',
        views.nano_banana_pro_guide,
        name='nano_banana_pro_guide'
    ),
    path(
        'guides/openclaw-miniqmt-trading/',
        views.openclaw_miniqmt_trading_guide,
        name='openclaw_miniqmt_trading_guide'
    ),
    path(
        'guides/openclaw-a-share-auto-trading/',
        views.openclaw_a_share_auto_trading_guide,
        name='openclaw_a_share_auto_trading_guide'
    ),
    path(
        'guides/openclaw-guardian-agent/',
        views.openclaw_guardian_agent_guide,
        name='openclaw_guardian_agent_guide'
    ),
    path(
        'guides/openclaw-ai-learning-workflow/',
        views.openclaw_ai_learning_workflow_guide,
        name='openclaw_ai_learning_workflow_guide'
    ),
    path(
        'guides/opencli-guide/',
        views.opencli_guide,
        name='opencli_guide'
    ),
    path(
        'guides/llm-algorithm-engineer-sources/',
        views.llm_algorithm_engineer_sources_guide,
        name='llm_algorithm_engineer_sources_guide'
    ),
    path(
        'guides/yaoban-research-learning-guide/',
        views.yaoban_research_learning_guide,
        name='yaoban_research_learning_guide'
    ),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('topics/', views.topic_list, name='topic_list'),
    re_path(r'^topics/(?P<slug>[\w\-\u4e00-\u9fff]+)/$', views.topic_detail, name='topic_detail'),
    path('trending/', views.trending_tools, name='trending_tools'),
    path('columns/trending/', views.trending_columns, name='trending_columns'),
    path('tools/', views.tool_list, name='tool_list'),
    re_path(r'^tools/(?P<slug>[\w\-\u4e00-\u9fff]+)/$', views.tool_detail, name='tool_detail'),
]
