from django.core.management.base import BaseCommand
from django.utils import timezone

from tools.models import TTSOrder


class Command(BaseCommand):
    help = '清理已过期的 TTS 交付音频文件。'

    def handle(self, *args, **options):
        expired_orders = TTSOrder.objects.filter(
            output_file__isnull=False,
            output_expires_at__isnull=False,
            output_expires_at__lte=timezone.now(),
        ).exclude(output_file='')

        cleaned_count = 0
        for order in expired_orders:
            file_name = order.output_file.name
            order.output_file.delete(save=False)
            timestamp = timezone.now().strftime('%F %T')
            log_parts = [part for part in [order.processing_log.strip(), f'{timestamp} 交付文件已过期并清理: {file_name}'] if part]
            order.output_file = ''
            order.output_duration_seconds = None
            order.processing_log = '\n'.join(log_parts)
            order.save(update_fields=['output_file', 'output_duration_seconds', 'processing_log', 'updated_at'])
            cleaned_count += 1

        self.stdout.write(self.style.SUCCESS(f'已清理 {cleaned_count} 个过期音频文件。'))
