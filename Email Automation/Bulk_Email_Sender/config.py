"""
========================================
BULK EMAIL CONFIGURATION
========================================
Edit this file to customize bulk email campaign settings.
All configurable parameters are here.
"""

# ========================================
# BREVO API CONFIGURATION
# ========================================
# Set your Brevo API key here OR as environment variable
BREVO_API_KEY = ""  # Leave empty to use environment variable BREVO_API_KEY

# ========================================
# SENDER INFORMATION
# ========================================
FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET CSE Fest 2026"

# ========================================
# REPLY-TO INFORMATION (Change per event/campaign)
# ========================================
REPLY_TO_EMAIL = "ctf@buetcsefest2026.com"
REPLY_TO_NAME = "CTF Team"

# ========================================
# EMAIL CONTENT
# ========================================
SUBJECT = "BUET CSE Fest 2026 – Update"

# Email body template
# Available variables: {team}, {message}, {reply_team}
BODY_TEXT_TEMPLATE = """\
Hello {team},

This is an update from BUET CSE Fest 2026.

{message}

If you have any questions, just reply to this email.

Regards,
{reply_team}
BUET CSE Fest 2026
"""

# Default message (can be overridden by EMAIL_MESSAGE environment variable)
DEFAULT_MESSAGE = "Registration deadline has been extended. Please check the portal for details."

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
# Paid plans: Can be faster, e.g., 0.3-0.5 seconds
SECONDS_BETWEEN_EMAILS = 0.3

# ========================================
# CSV COLUMN NAMES
# ========================================
# If your CSV has different column names, change them here
EMAIL_COL = "Email address"
TEAM_COL = "Team Name"
SEND_NOW_COL = "Send Now"
MAIL_SENT_COL = "Mail Sent"
