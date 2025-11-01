from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from notifier.services import get_all_rows
from notifier.models import ReminderLog
import os


class Command(BaseCommand):
    help = 'Send daily contribution balance reminders to all group members'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print emails without sending them',
        )
        parser.add_argument(
            '--only',
            nargs='*',
            help='Limit sending to one or more member names (e.g., --only Allan Blessing). Case-insensitive.',
        )
        parser.add_argument(
            '--override-email',
            help='Send all selected reminders to this single email address (useful for testing).',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        only_members = options.get('only') or []
        override_email = options.get('override_email')
        
        # Member email addresses (update these with actual emails)
        members = {
            'sultan': os.getenv('SULTAN_EMAIL', 'sultan@example.com'),
            'Blessing': os.getenv('BLESSING_EMAIL', 'blessing@example.com'),
            'cynthia': os.getenv('CYNTHIA_EMAIL', 'cynthia@example.com'),
            'Allan': os.getenv('ALLAN_EMAIL', 'allan@example.com'),
        }

        # Filter members if --only was provided (case-insensitive match)
        if only_members:
            wanted = {name.lower() for name in only_members}
            members = {k: v for k, v in members.items() if k.lower() in wanted}
            if not members:
                self.stdout.write(self.style.ERROR('No matching members found for --only'))
                return
        
        try:
            # Define expected headers to handle duplicate column names
            expected_headers = [
                'Date', 'sultan', 'Blessing', 'cynthia', 'Allan',
                'challenge', 'sultan running', 'blessing running', 
                'cynthia running', 'Allan running'
            ]
            
            # Fetch contribution data from Google Sheets
            contributions = get_all_rows(
                "money mates tracker", 
                "daily log",
                expected_headers=expected_headers
            )
            
            if not contributions:
                self.stdout.write(self.style.ERROR('No contribution data found'))
                return
            
            # Map member names to their running balance keys (case-sensitive as per sheet)
            running_key_map = {
                'sultan': 'sultan running',
                'Blessing': 'blessing running',  # lowercase 'b' in sheet
                'cynthia': 'cynthia running',
                'Allan': 'Allan running',
            }

            # Get latest balances for each member
            latest_data = {}
            for member in members.keys():
                running_key = running_key_map.get(member, f"{member} running")
                contrib_key = member
                
                # Get the last non-empty balance
                latest_balance = "0"
                latest_contribution = "-"
                latest_date = "Unknown"
                
                for row in reversed(contributions):
                    balance_val = str(row.get(running_key, '')).strip()
                    if balance_val and latest_balance == "0":
                        latest_balance = balance_val
                    
                    contrib_val = str(row.get(contrib_key, '')).strip()
                    if contrib_val and latest_contribution == "-":
                        latest_contribution = contrib_val
                    
                    date_val = str(row.get('Date', '')).strip()
                    if date_val and latest_date == "Unknown":
                        latest_date = date_val
                    
                    # Break if we have all data
                    if latest_balance != "0" and latest_contribution != "-":
                        break
                
                latest_data[member] = {
                    'balance': latest_balance,
                    'last_contribution': latest_contribution,
                    'date': latest_date
                }
            
            # Send emails to each member
            emails_sent = 0
            for member, email in members.items():
                data = latest_data[member]
                balance = data['balance']
                is_deficit = '-' in balance
                
                # Create personalized message
                subject = f"💰 Daily Balance Update - {member.capitalize()}"
                
                message = f"""Hello {member.capitalize()},

Here's your daily contribution update:

Current Balance: {balance}
Status: {"⚠️ DEFICIT" if is_deficit else "✅ Good Standing"}
Last Contribution: {data['last_contribution']}
Last Updated: {data['date']}

"""
                
                # Add summary of all members
                message += "\n📊 Group Summary:\n"
                message += "-" * 40 + "\n"
                for m, d in latest_data.items():
                    status = "🔴" if '-' in d['balance'] else "🟢"
                    message += f"{status} {m.capitalize()}: {d['balance']}\n"
                
                message += "\n" + "-" * 40 + "\n"
                
                if is_deficit:
                    message += "\n⚠️ You have a deficit. Please contribute to catch up!\n"
                else:
                    message += "\n✅ Great job staying on track!\n"
                
                message += f"\nView full tracker: {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}\n"
                message += "\n--\nMoney Mates Tracker\nAutomated Daily Reminder"
                
                # For testing, optionally override the recipient email
                target_email = override_email or email

                if dry_run:
                    self.stdout.write(self.style.WARNING(f'\n[DRY RUN] Would send to {target_email}:'))
                    self.stdout.write(subject)
                    self.stdout.write(message)
                    self.stdout.write('-' * 60)
                else:
                    try:
                        # Check if we're using console backend (dev mode)
                        using_console = 'console' in settings.EMAIL_BACKEND.lower()
                        
                        num_sent = send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [target_email],
                            fail_silently=False,
                        )
                        
                        if using_console:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'⚠️ Email printed to console (not sent) for {member} - '
                                    f'Set EMAIL_BACKEND to smtp in .env to actually send'
                                )
                            )
                            # Don't log as success if using console backend
                        elif num_sent > 0:
                            emails_sent += 1
                            self.stdout.write(self.style.SUCCESS(f'✓ Sent reminder to {member} at {target_email}'))
                            
                            # Log successful send (no email address stored)
                            ReminderLog.objects.create(
                                member_name=member,
                                status='success',
                                balance_shown=balance
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'⚠️ send_mail returned 0 for {member} (email may not have been sent)')
                            )
                            
                    except Exception as e:
                        error_msg = str(e)
                        self.stdout.write(
                            self.style.ERROR(f'✗ Failed to send to {member}: {error_msg}')
                        )
                        
                        # Log failed send attempt (no email address stored)
                        ReminderLog.objects.create(
                            member_name=member,
                            status='failed',
                            balance_shown=balance,
                            error_message=error_msg
                        )
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(f'\n[DRY RUN] Would have sent {len(members)} emails')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'\n✓ Successfully sent {emails_sent}/{len(members)} reminder emails')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching contribution data: {str(e)}')
            )
            raise
