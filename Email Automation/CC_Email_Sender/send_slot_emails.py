#!/usr/bin/env python3
"""Send slot allocation and payment emails to university coaches."""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file in parent directory
try:
    from dotenv import load_dotenv
    # Get the parent directory of the current script
    parent_dir = Path(__file__).resolve().parent.parent
    env_path = parent_dir / '.env'
    load_dotenv(env_path)
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    # Continue anyway, maybe the env var is already set

try:
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
except ImportError:
    print("Error: sib-api-v3-sdk not installed. Install with: pip install sib-api-v3-sdk")
    sys.exit(1)

# Import configuration
try:
    import iupc_slot_config as config
except ImportError:
    print("Error: iupc_slot_config.py not found")
    sys.exit(1)


def get_short_university_name(university_name):
    """Get a shortened version of university name for reference."""
    # Remove common words
    words = university_name.replace('UNIVERSITY', '').replace('OF', '').split()
    # Take first few meaningful words
    short = ' '.join(words[:3]).strip()
    return short if short else university_name[:20]


def format_team_list_text(teams):
    """Format team list for plain text email."""
    return '\n'.join([f"  • {team['team_name']}" for team in teams])


def format_team_list_html(teams):
    """Format team list for HTML email."""
    return '<ul style="margin: 10px 0;">' + ''.join([
        f'<li style="margin: 5px 0;">{team["team_name"]}</li>' 
        for team in teams
    ]) + '</ul>'


def format_account_holder_info_text(holder_name):
    """Format account holder info for text email."""
    if holder_name:
        return f"📝 Account holder: {holder_name}"
    return ""


def format_account_holder_info_html(holder_name):
    """Format account holder info for HTML email."""
    if holder_name:
        return f'<div class="payment-detail"><strong>📝 Account holder:</strong> {holder_name}</div>'
    return ""


def prepare_email_content(university_data):
    """Prepare email content for a university."""
    university = university_data['university']
    allocated_slots = university_data['allocated_slots']
    team_count = university_data['team_count']
    teams = university_data['teams']
    payment_info = university_data.get('payment_info', {})
    
    bkash_account = payment_info.get('bkash_account', 'NOT ASSIGNED')
    account_holder_name = payment_info.get('account_holder_name', '')
    
    per_team_amount = config.PER_TEAM_AMOUNT
    total_amount = per_team_amount * allocated_slots
    
    # Format team lists
    team_list_text = format_team_list_text(teams)
    team_list_html = format_team_list_html(teams)
    
    # Format account holder info
    account_holder_info_text = format_account_holder_info_text(account_holder_name)
    account_holder_info_html = format_account_holder_info_html(account_holder_name)
    
    university_short = get_short_university_name(university)
    
    # Prepare template variables
    template_vars = {
        'university': university,
        'allocated_slots': allocated_slots,
        'team_count': team_count,
        'team_list': team_list_text,
        'team_list_html': team_list_html,
        'bkash_account': bkash_account,
        'account_holder_name': account_holder_name,
        'account_holder_info': account_holder_info_text,
        'account_holder_info_html': account_holder_info_html,
        'total_amount': f"{total_amount:,}",
        'per_team_amount': f"{per_team_amount:,}",
        'university_short': university_short,
        'contact_email': config.CONTACT_EMAIL,
    }
    
    # Format email content
    subject = config.SUBJECT.format(**template_vars)
    text_content = config.BODY_TEXT_TEMPLATE.format(**template_vars)
    html_content = config.BODY_HTML_TEMPLATE.format(**template_vars)
    
    return subject, text_content, html_content


def send_email(api_instance, university_data, test_mode=False):
    """Send email to university coaches."""
    coach_emails = university_data['coach_emails']
    university = university_data['university']
    
    if not coach_emails:
        print(f"⚠ Skipping {university}: No coach emails")
        return False
    
    # Prepare email content
    subject, text_content, html_content = prepare_email_content(university_data)
    
    # Prepare recipients
    if test_mode:
        # In test mode, send only to the test email but show university info
        to_recipients = [{"email": config.TEST_TO, "name": f"Test - {university}"}]
        print(f"\n🧪 TEST MODE: Sending email for {university} to {config.TEST_TO}")
    else:
        # First coach is primary recipient
        to_recipients = [{"email": coach_emails[0]}]
        print(f"\n📧 Sending to {university}")
        print(f"   Primary: {coach_emails[0]}")
    
    # Rest are CC'd
    cc_recipients = []
    if not test_mode and len(coach_emails) > 1:
        cc_recipients = [{"email": email} for email in coach_emails[1:]]
        print(f"   CC: {', '.join(coach_emails[1:])}")
    
    # Add global CC emails
    for email in config.GLOBAL_CC_EMAILS:
        cc_recipients.append({"email": email})
    
    # Prepare sender
    sender = {"name": config.FROM_NAME, "email": config.FROM_EMAIL}
    reply_to = {"name": config.REPLY_TO_NAME, "email": config.REPLY_TO_EMAIL}
    
    # Create email
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to_recipients,
        cc=cc_recipients if cc_recipients else None,
        sender=sender,
        reply_to=reply_to,
        subject=subject,
        text_content=text_content,
        html_content=html_content
    )
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"   ✅ Sent successfully (Message ID: {api_response.message_id})")
        return True
    except ApiException as e:
        print(f"   ❌ Failed: {e}")
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(description='Send slot allocation emails')
    parser.add_argument('--json', default='university_teams_with_payment.json',
                       help='JSON file with university data')
    parser.add_argument('--test', action='store_true',
                       help='Test mode: Send only BUET email to test address')
    parser.add_argument('--dry-run', action='store_true',
                       help='Dry run: Show what would be sent without sending')
    parser.add_argument('--delay', type=float, default=None,
                       help='Delay between emails in seconds (default: from config)')
    args = parser.parse_args(argv)
    
    # Load universities data
    if not os.path.isfile(args.json):
        print(f"Error: JSON file not found: {args.json}")
        return 1
    
    with open(args.json, 'r', encoding='utf-8') as f:
        universities = json.load(f)
    
    # Test mode: filter to only BUET
    if args.test:
        buet_data = [u for u in universities if u['university'] == 'BUET']
        if not buet_data:
            print("Error: BUET entry not found in JSON for test mode")
            return 2
        universities = buet_data
        print(f"\n🧪 TEST MODE ENABLED")
        print(f"   Will send only BUET email to: {config.TEST_TO}")
        print(f"   (In production, would send to all {len(universities)} universities)")
    
    print(f"\n📊 Summary:")
    print(f"   Universities to email: {len(universities)}")
    print(f"   Test mode: {'YES' if args.test else 'NO'}")
    print(f"   Dry run: {'YES' if args.dry_run else 'NO'}")
    
    if args.dry_run:
        print("\n📝 DRY RUN - No emails will be sent\n")
        for uni in universities:
            subject, text, html = prepare_email_content(uni)
            print(f"\n{'='*60}")
            print(f"University: {uni['university']}")
            print(f"To: {uni['coach_emails'][0]}")
            if len(uni['coach_emails']) > 1:
                print(f"CC: {', '.join(uni['coach_emails'][1:])}")
            print(f"Subject: {subject}")
            print(f"\n{text[:500]}...")
        return 0
    
    # Get API key
    api_key = config.BREVO_API_KEY or os.getenv('BREVO_API_KEY')
    if not api_key:
        print("Error: BREVO_API_KEY not set in config or environment")
        return 3
    
    # Configure API
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
    
    # Send emails
    delay = args.delay if args.delay is not None else config.SECONDS_BETWEEN_EMAILS
    
    print(f"\n{'='*60}")
    print(f"Starting email send at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    sent = 0
    failed = 0
    
    for i, uni in enumerate(universities):
        if send_email(api_instance, uni, test_mode=args.test):
            sent += 1
        else:
            failed += 1
        
        # Delay between emails (except for the last one)
        if i < len(universities) - 1:
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"✅ Sent: {sent}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(universities)}")
    
    return 0 if failed == 0 else 4


if __name__ == '__main__':
    sys.exit(main())
