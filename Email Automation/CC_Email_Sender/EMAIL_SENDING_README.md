# BUET IUPC 2026 - Slot Allocation Email System

This system sends slot allocation and payment instruction emails to university coaches.

## Files

- `iupc_slot_config.py` - Email template and configuration
- `send_slot_emails.py` - Email sending script
- `university_teams_with_payment.json` - University data with payment info
- `split_universities_by_slots.py` - Split universities by allocated slots
- `add_payment_info.py` - Add payment info to JSON
- `fix_bkash.py` - Normalize Bkash numbers (prepend 0 if needed)

## Setup

1. Install dependencies:
```bash
pip install sib-api-v3-sdk
```

2. Set your Brevo API key in `iupc_slot_config.py` or as environment variable:
```bash
export BREVO_API_KEY="your-api-key-here"
```

3. Configure email settings in `iupc_slot_config.py`:
   - Sender information
   - Contact email
   - Test mode settings
   - Rate limiting

## Usage

### Test Mode (Recommended First)

Send only BUET email to test address to verify everything works:

```bash
python3 send_slot_emails.py --test --dry-run
```

This shows what would be sent without actually sending. Remove `--dry-run` to actually send:

```bash
python3 send_slot_emails.py --test
```

### Production Mode

Send emails to all universities:

```bash
# First, do a dry run to review
python3 send_slot_emails.py --dry-run

# Then send for real
python3 send_slot_emails.py
```

### Options

- `--test` - Send only BUET email to test address (amimul.ehsan2001@gmail.com)
- `--dry-run` - Show what would be sent without sending
- `--delay SECONDS` - Override delay between emails (default: from config)
- `--json FILE` - Use different JSON file (default: university_teams_with_payment.json)

### Examples

```bash
# Test with custom delay
python3 send_slot_emails.py --test --delay 0.5

# Production with 2 second delay
python3 send_slot_emails.py --delay 2.0

# Use different JSON file
python3 send_slot_emails.py --json university_teams_custom.json
```

## Email Features

### Personalized Content
- University name
- Allocated slots count
- List of registered teams
- Specific bKash account number for payment
- Account holder name (if available)
- Total amount calculation

### Professional Formatting
- Plain text version for compatibility
- Rich HTML version with styling
- Step-by-step registration instructions
- Important warnings and deadlines highlighted
- Clickable links to forms and documents

### CC Handling
- Primary coach receives as "To"
- Other coaches automatically CC'd
- Maintains professional communication

## Test Mode Details

When `--test` flag is used:
- Only BUET entry is processed
- Email sent to `amimul.ehsan2001@gmail.com` (configurable in `iupc_slot_config.py`)
- Subject line shows it's for BUET
- All coach emails would normally be CC'd are not sent in test mode
- Perfect for verifying email content and API integration

## Data Preparation

### 1. Fix Bkash Numbers
```bash
python3 fix_bkash.py Final_Slot_With_Bkash.csv --inplace
```

### 2. Split Universities by Slots
```bash
python3 split_universities_by_slots.py
```
This creates:
- `university_teams_with_payment.json` - Universities with allocated slots > 0
- `university_teams_zero_slots.json` - Universities with 0 slots (no email needed)

## Configuration

Edit `iupc_slot_config.py` to customize:

```python
# Email sender
FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET IUPC 2026"

# Test settings
TEST_MODE = False  # Controlled by --test flag
TEST_TO = "amimul.ehsan2001@gmail.com"

# Payment
PER_TEAM_AMOUNT = 5500  # BDT per team

# Rate limiting
SECONDS_BETWEEN_EMAILS = 1.0  # Adjust based on your plan
```

## Important Notes

⚠️ **Before Production Send:**
1. Always test with `--test --dry-run` first
2. Verify email content looks correct
3. Check all links work
4. Confirm bKash numbers are correct (11 digits starting with 0)
5. Review deadline date in email

⚠️ **Rate Limits:**
- Free Brevo plan: 300 emails/day
- Adjust `SECONDS_BETWEEN_EMAILS` as needed
- Use `--delay` flag to override

⚠️ **Email Validation:**
- Script validates coach emails exist
- Skips universities with no coach emails
- Reports success/failure for each send

## Troubleshooting

**"BREVO_API_KEY not set"**
- Add API key to `iupc_slot_config.py` or set environment variable

**"sib-api-v3-sdk not installed"**
- Run: `pip install sib-api-v3-sdk`

**Rate limit errors**
- Increase delay: `--delay 2.0`
- Check your Brevo plan limits

**BUET not found in test mode**
- Ensure BUET entry exists in JSON file
- Check university name matches exactly: "BUET"

## Email Content Summary

Each email includes:
1. ✅ Slot allocation announcement
2. 📊 Link to complete allocation PDF
3. 👥 List of registered teams
4. 💳 Payment instructions (per team, separately)
5. 📝 Team information form link
6. ⏰ Deadline (26 January 2026, 11:55 PM)
7. 📄 Payment tracking sheet link
8. 📧 Contact information

## Support

For issues or questions: iupc@buetcsefest2026.com
