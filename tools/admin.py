from django.contrib import admin, messages
from django.utils import timezone

from .models import Category, Tool, TopicPage, ToolDailyView, TTSOrder, TTSCreditAccount, TTSCreditRechargeOrder, TTSCreditLedger
from .tts_jobs import trigger_tts_generation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'is_published', 'created_at']
    list_filter = ['category', 'is_featured', 'is_published', 'created_at']
    search_fields = ['name', 'short_description', 'full_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_published']
    ordering = ['-created_at']


@admin.register(TopicPage)
class TopicPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'updated_at']
    search_fields = ['title', 'meta_description', 'intro']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_published', 'updated_at']
    filter_horizontal = ['categories']
    ordering = ['-updated_at']


@admin.register(ToolDailyView)
class ToolDailyViewAdmin(admin.ModelAdmin):
    list_display = ['tool', 'date', 'count', 'updated_at']
    search_fields = ['tool__name']
    list_filter = ['date']
    ordering = ['-date', '-count']


@admin.action(description='标记为已付款并进入待生成队列')
def mark_paid_and_queue(modeladmin, request, queryset):
    now = timezone.now()
    order_nos = list(queryset.values_list('order_no', flat=True))
    queryset.update(
        payment_status=TTSOrder.PaymentStatus.PAID,
        status=TTSOrder.Status.QUEUED,
        payment_verified_at=now,
        paid_at=now,
    )
    for order_no in order_nos:
        trigger_tts_generation(order_no)


@admin.register(TTSOrder)
class TTSOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_no', 'contact_name', 'char_count', 'estimated_price', 'payment_provider',
        'payment_reference', 'payment_status', 'status', 'created_at'
    ]
    list_filter = ['voice_preset', 'payment_status', 'status', 'business_usage', 'delivery_format']
    search_fields = ['order_no', 'contact_name', 'email', 'wechat', 'company', 'source_text']
    readonly_fields = [
        'order_no', 'char_count', 'estimated_price', 'payment_note_token', 'payment_reference',
        'payment_verified_at', 'output_duration_seconds', 'payment_proof_uploaded_at', 'created_at', 'updated_at'
    ]
    actions = [mark_paid_and_queue]
    ordering = ['-created_at']


@admin.register(TTSCreditAccount)
class TTSCreditAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_unlimited', 'char_balance', 'total_purchased_chars', 'total_used_chars', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TTSCreditRechargeOrder)
class TTSCreditRechargeOrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'user', 'char_amount', 'amount', 'payment_status', 'payment_provider', 'created_at']
    list_filter = ['payment_status', 'payment_provider', 'created_at']
    search_fields = ['order_no', 'user__username', 'user__email', 'payment_reference', 'payment_note_token']
    readonly_fields = ['order_no', 'payment_note_token', 'created_at', 'updated_at', 'paid_at', 'payment_verified_at']

    @admin.action(description='确认到账并自动发放字数额度')
    def confirm_recharge(self, request, queryset):
        confirmed = 0
        for order in queryset:
            if order.payment_status == TTSCreditRechargeOrder.PaymentStatus.PAID:
                continue

            account, _ = TTSCreditAccount.objects.get_or_create(user=order.user)
            account.char_balance += order.char_amount
            account.total_purchased_chars += order.char_amount
            account.save(update_fields=['char_balance', 'total_purchased_chars', 'updated_at'])

            TTSCreditLedger.objects.create(
                user=order.user,
                entry_type=TTSCreditLedger.EntryType.RECHARGE,
                char_delta=order.char_amount,
                balance_after=account.char_balance,
                recharge_order=order,
                note=f'后台确认到账，发放 {order.char_amount} 字',
            )

            order.payment_status = TTSCreditRechargeOrder.PaymentStatus.PAID
            order.payment_provider = TTSCreditRechargeOrder.PaymentProvider.WECHAT
            order.paid_at = timezone.now()
            order.payment_verified_at = timezone.now()
            order.save(update_fields=['payment_status', 'payment_provider', 'paid_at', 'payment_verified_at', 'updated_at'])
            confirmed += 1

        self.message_user(request, f'已确认 {confirmed} 笔充值到账。', level=messages.SUCCESS)

    actions = ['confirm_recharge']


@admin.register(TTSCreditLedger)
class TTSCreditLedgerAdmin(admin.ModelAdmin):
    list_display = ['user', 'entry_type', 'char_delta', 'balance_after', 'created_at']
    list_filter = ['entry_type', 'created_at']
    search_fields = ['user__username', 'note']
    readonly_fields = ['created_at']
