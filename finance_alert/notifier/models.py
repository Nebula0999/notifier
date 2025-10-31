from django.db import models


class ReminderLog(models.Model):
    """
    Log of sent reminder emails.
    
    For data protection, only stores member names and status.
    Does NOT store email addresses or message content.
    """
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    member_name = models.CharField(
        max_length=100,
        help_text="Name of the member who received the reminder"
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the reminder was sent"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='success',
        help_text="Whether the email was sent successfully"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text="Error details if the send failed"
    )
    balance_shown = models.CharField(
        max_length=50,
        blank=True,
        help_text="The balance value shown in the reminder (for reference)"
    )
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Reminder Log"
        verbose_name_plural = "Reminder Logs"
    
    def __str__(self):
        return f"{self.member_name} - {self.sent_at.strftime('%Y-%m-%d %H:%M')} ({self.status})"
