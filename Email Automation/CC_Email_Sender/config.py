"""
========================================
EMAIL CONFIGURATION
========================================
Edit this file to customize your email settings.
All configurable parameters are here.
"""

# ========================================
# BREVO API CONFIGURATION
# ========================================
# Set your Brevo API key here OR as environment variable
# Get your API key from: https://app.brevo.com/settings/keys/api
BREVO_API_KEY = ""  # Leave empty to use environment variable BREVO_API_KEY

# ========================================
# SENDER INFORMATION
# ========================================
FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET CSE Fest 2026"

# ========================================
# REPLY-TO INFORMATION
# ========================================
REPLY_TO_EMAIL = "iupc@buetcsefest2026.com"
REPLY_TO_NAME = "IUPC Team"

# ========================================
# EMAIL CONTENT
# ========================================
SUBJECT = "BUET CSE Fest 2026 – Testing CC Feature"

# Email body template
# Available variables: {recipient_name}, {team}, {message}, {reply_team}, {contact_email}
BODY_TEXT_TEMPLATE = """\
Hello {recipient_name},

This is an important update from BUET CSE Fest 2026.

{message}

If you have any questions, just contact us.

Best regards,
{reply_team}
BUET CSE Fest 2026
Contact: {contact_email}
"""

# Default message (can be overridden by EMAIL_MESSAGE environment variable)
DEFAULT_MESSAGE = "Slot has been allocated. Please check the drive link for details."

# ========================================
# GLOBAL CC RECIPIENTS
# ========================================
# Add emails here that should be CC'd on EVERY email sent
# Example: ["amimul.ehsan2001@gmail.com", "another@email.com"]
GLOBAL_CC_EMAILS = []

# To add CC to specific emails, use the CSV file's "CC Emails" column

# ========================================
# TESTING CONFIGURATION
# ========================================
# Set TEST_MODE = True to send all emails to TEST_TO address
TEST_MODE = False
TEST_TO = "amimul.ehsan2001@gmail.com"

# ========================================
# RATE LIMITING
# ========================================
# Delay between emails in seconds (adjust based on your Brevo plan)
# Free plan: 300 emails/day, Recommended: 1.0-2.0 seconds
# Paid plans: Can be faster, e.g., 0.1-0.3 seconds
SECONDS_BETWEEN_EMAILS = 0.1

# ========================================
# CSV COLUMN NAMES
# ========================================
# If your CSV has different column names, change them here
RECIPIENT_EMAIL_COL = "Recipient Email"
RECIPIENT_NAME_COL = "Recipient Name"
TEAM_COL = "Team Name"
CC_EMAILS_COL = "CC Emails"  # Comma-separated CC emails per row
SEND_NOW_COL = "Send Now"
MAIL_SENT_COL = "Mail Sent"
