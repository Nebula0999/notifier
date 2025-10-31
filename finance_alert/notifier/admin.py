from django.contrib import admin
from .models import ReminderLog


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing reminder send history.
    """
    list_display = ['member_name', 'sent_at', 'status', 'balance_shown']
    list_filter = ['status', 'member_name', 'sent_at']
    search_fields = ['member_name', 'error_message']
    readonly_fields = ['member_name', 'sent_at', 'status', 'error_message', 'balance_shown']
    date_hierarchy = 'sent_at'
    
    def has_add_permission(self, request):
        """Disable manual creation - logs are auto-generated only."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make logs read-only."""
        return False
