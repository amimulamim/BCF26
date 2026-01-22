"""
========================================
BUET IUPC 2026 - SLOT ALLOCATION EMAIL CONFIGURATION
========================================
Email configuration for slot allocation and payment instructions.
"""

# ========================================
# BREVO API CONFIGURATION
# ========================================
BREVO_API_KEY = ""  # Leave empty to use environment variable BREVO_API_KEY

# ========================================
# SENDER INFORMATION
# ========================================
FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET IUPC 2026"

# ========================================
# REPLY-TO INFORMATION
# ========================================
REPLY_TO_EMAIL = "iupc@buetcsefest2026.com"
REPLY_TO_NAME = "IUPC Organizing Team"

# ========================================
# EMAIL CONTENT
# ========================================
SUBJECT = "BUET IUPC 2026 – Slot Allocation & Payment Instructions for {university}"

# Email body template
# Available variables: 
#   {university} - University name
#   {allocated_slots} - Number of allocated slots
#   {team_count} - Total number of registered teams
#   {team_list} - Formatted list of team names
#   {bkash_account} - Bkash account number for payment
#   {account_holder_name} - Bkash account holder name (optional)
#   {total_amount} - Total payment amount (5500 × allocated_slots)
#   {per_team_amount} - Per team amount (5500 BDT)

BODY_TEXT_TEMPLATE = """\
Dear Coaches,

Greetings from BUET IUPC 2026!

We are pleased to inform you that {university} has been allocated {allocated_slots} slot(s) for the final round of BUET IUPC 2026.

📊 SLOT ALLOCATION OVERVIEW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Slot allocation has been determined based on performance in previous contests and other relevant factors. Please note that the cheater list from the last ICPC Preliminary was taken into serious consideration.

Complete Slot Allocation PDF:
https://drive.google.com/file/d/1p8X3QLlnyqvJumvuiCJgRtLSKxtiva7h/view?usp=sharing

Your university registered a total of {team_count} team(s):
{team_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ FINAL REGISTRATION STEPS (MUST FOLLOW)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Confirm Team Selection
Please confirm which {allocated_slots} team(s) from your university will participate in the final round.

STEP 2: Pay Registration Fee (EACH TEAM SEPARATELY)
💳 Amount per team: {per_team_amount} BDT
📱 bKash number: {bkash_account}
{account_holder_info}

⚠️ CRITICAL: Each team must pay SEPARATELY. Do NOT combine payments.
   • Each team sends {per_team_amount} BDT individually
   • Total expected: {allocated_slots} separate transactions = {total_amount} BDT
   
✍️ IMPORTANT: During each bKash payment, the team MUST write their Team Name in the reference field.
🧾 Each team must save their Transaction ID (TrxID) - it is mandatory for the next step.

⚠️ DO NOT send money to any other number. Only use the bKash number mentioned above.

STEP 3: Submit Team Information Form (EACH TEAM SEPARATELY)
After completing the payment, EACH team must fill out the Team Information Form separately:

📝 Team Information Form:
https://forms.gle/CNGLm7kC9gu5GicWA

Required information (per team):
  • Transaction ID (TrxID) - unique for each team's payment
  • Recipient Phone Number (bKash number you paid to)
  • Team details (some universities may reform their teams)

⚠️ NOTE: Each team must submit this form separately with their own transaction ID.

⏰ DEADLINE: 26 January 2026, 11:55 PM (for all teams)

STEP 4: Verify Payment Acknowledgement
After submitting the form, you can check the payment acknowledgement in our tracking sheet:

📄 Payment Acknowledgement Sheet:
https://docs.google.com/spreadsheets/d/1QfdwR0fsvNdsGWkPC1OfhucjXlW1nYi40fUqtB6OTAw/edit?usp=sharing

⏳ Please note: It may take 1-2 days for the sheet to update after form submission.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you have any questions or need clarification, please feel free to contact us at {contact_email}.

We look forward to your participation in BUET IUPC 2026!

Best regards,
BUET IUPC 2026 Organizing Committee
BUET CSE Fest 2026

Contact: {contact_email}
Website: https://buetcsefest2026.com
"""

# HTML email template (optional, for better formatting)
BODY_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 650px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #0066cc; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
        .content {{ background-color: #f9f9f9; padding: 30px; border: 1px solid #ddd; }}
        .info-box {{ background-color: #e7f3ff; border-left: 4px solid #0066cc; padding: 15px; margin: 20px 0; }}
        .team-list {{ background-color: white; padding: 15px; margin: 15px 0; border-left: 4px solid #0066cc; }}
        .step-box {{ background-color: white; border: 2px solid #ddd; padding: 20px; margin: 15px 0; border-radius: 5px; }}
        .step-box h3 {{ margin-top: 0; color: #0066cc; }}
        .payment-box {{ background-color: #fff3cd; border: 2px solid #ffc107; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .payment-detail {{ margin: 10px 0; font-size: 16px; }}
        .payment-detail strong {{ display: inline-block; width: 180px; }}
        .warning {{ background-color: #f8d7da; border: 2px solid #dc3545; padding: 15px; margin: 15px 0; border-radius: 5px; color: #721c24; }}
        .deadline {{ background-color: #fff3cd; border: 2px solid #ff6b6b; padding: 15px; margin: 15px 0; border-radius: 5px; font-weight: bold; text-align: center; font-size: 18px; color: #721c24; }}
        .footer {{ background-color: #333; color: white; padding: 20px; text-align: center; border-radius: 0 0 5px 5px; margin-top: 20px; }}
        .footer a {{ color: #66ccff; text-decoration: none; }}
        .link-button {{ display: inline-block; background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 8px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 BUET IUPC 2026</h1>
            <p>Slot Allocation & Final Registration</p>
        </div>
        
        <div class="content">
            <p>Dear Coaches,</p>
            
            <p>Greetings from BUET IUPC 2026!</p>
            
            <p>We are pleased to inform you that <strong style="color: #0066cc;">{university}</strong> has been allocated <strong style="color: #0066cc; font-size: 18px;">{allocated_slots} slot(s)</strong> for the final round of BUET IUPC 2026.</p>
            
            <div class="info-box">
                <p><strong>📊 Slot Allocation Overview</strong></p>
                <p>Slot allocation has been determined based on performance in previous contests and other relevant factors. Please note that the cheater list from the last ICPC Preliminary was taken into serious consideration.</p>
                <p><a href="https://drive.google.com/file/d/1p8X3QLlnyqvJumvuiCJgRtLSKxtiva7h/view?usp=sharing" class="link-button">📄 View Complete Slot Allocation PDF</a></p>
            </div>
            
            <div class="team-list">
                <p><strong>Your university registered {team_count} team(s):</strong></p>
                {team_list_html}
            </div>
            
            <h2 style="color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px;">✅ Final Registration Steps</h2>
            
            <div class="step-box">
                <h3>STEP 1: Confirm Team Selection</h3>
                <p>Please confirm which <strong>{allocated_slots} team(s)</strong> from your university will participate in the final round.</p>
            </div>
            
            <div class="step-box">
                <h3>STEP 2: Pay Registration Fee (EACH TEAM SEPARATELY)</h3>
                <div class="payment-box">
                    <div class="payment-detail"><strong>💳 Amount per team:</strong> {per_team_amount} BDT</div>
                    <div class="payment-detail"><strong>📱 bKash number:</strong> <span style="font-size: 18px; color: #0066cc; font-weight: bold;">{bkash_account}</span></div>
                    {account_holder_info_html}
                    <div class="payment-detail"><strong>💰 Total expected:</strong> {allocated_slots} separate transactions = <span style="font-size: 20px; color: #856404;">{total_amount} BDT</span></div>
                </div>
                <div class="warning" style="background-color: #fff3cd; border-color: #ffc107; color: #856404;">
                    <strong>⚠️ CRITICAL:</strong> Each team must pay SEPARATELY. Do NOT combine payments.<br>
                    • Each team sends {per_team_amount} BDT individually<br>
                    • Each payment must have the team's name in reference field<br>
                    • Each team will have their own unique Transaction ID
                </div>
                <div class="warning">
                    <strong>⚠️ WARNING:</strong> DO NOT send money to any other number. Only use the bKash number mentioned above.
                </div>
            </div>
            
            <div class="step-box">
                <h3>STEP 3: Submit Team Information Form (EACH TEAM SEPARATELY)</h3>
                <p>After completing the payment, <strong>EACH team must fill out the form separately</strong>:</p>
                <p><a href="https://forms.gle/CNGLm7kC9gu5GicWA" class="link-button">📝 Fill Team Information Form</a></p>
                <p><strong>Required information (per team):</strong></p>
                <ul>
                    <li>Transaction ID (TrxID) - <em>unique for each team's payment</em></li>
                    <li>Recipient Phone Number (bKash number you paid to)</li>
                    <li>Team details (some universities may reform their teams)</li>
                </ul>
                <div class="warning" style="background-color: #e7f3ff; border-color: #0066cc; color: #004085;">
                    <strong>📝 NOTE:</strong> Each team must submit this form separately with their own transaction ID.
                </div>
            </div>
            
            <div class="deadline">
                ⏰ DEADLINE: 26 January 2026, 11:55 PM (for all teams)
            </div>
            
            <div class="step-box">
                <h3>STEP 4: Verify Payment Acknowledgement</h3>
                <p>After submitting the form, you can check the payment acknowledgement in our tracking sheet:</p>
                <p><a href="https://docs.google.com/spreadsheets/d/1QfdwR0fsvNdsGWkPC1OfhucjXlW1nYi40fUqtB6OTAw/edit?usp=sharing" class="link-button">📄 Check Payment Acknowledgement Sheet</a></p>
                <p><em>⏳ Please note: It may take 1-2 days for the sheet to update after form submission.</em></p>
            </div>
            
            <hr style="border: 1px solid #ddd; margin: 30px 0;">
            
            <p>If you have any questions or need clarification, please feel free to contact us at <a href="mailto:{contact_email}">{contact_email}</a>.</p>
            
            <p><strong>We look forward to your participation in BUET IUPC 2026!</strong></p>
            
            <p><strong>Best regards,</strong><br>
            BUET IUPC 2026 Organizing Committee<br>
            BUET CSE Fest 2026</p>
        </div>
        
        <div class="footer">
            <p><strong>📧 Contact:</strong> {contact_email}</p>
            <p><strong>🌐 Website:</strong> <a href="https://buetcsefest2026.com">buetcsefest2026.com</a></p>
        </div>
    </div>
</body>
</html>
"""

# ========================================
# PAYMENT CONFIGURATION
# ========================================
PER_TEAM_AMOUNT = 5500  # BDT per team

# ========================================
# GLOBAL CC RECIPIENTS
# ========================================
# Add organizing committee emails to CC on every email
GLOBAL_CC_EMAILS = []  # Example: ["amimul.ehsan2001@gmail.com"]

# ========================================
# TESTING CONFIGURATION
# ========================================
TEST_MODE = False
TEST_TO = "amimul.ehsan2001@gmail.com"

# ========================================
# RATE LIMITING
# ========================================
SECONDS_BETWEEN_EMAILS = 1.0  # Adjust based on your Brevo plan

# ========================================
# CONTACT INFORMATION
# ========================================
CONTACT_EMAIL = "iupc@buetcsefest2026.com"
WEBSITE = "https://buetcsefest2026.com"
