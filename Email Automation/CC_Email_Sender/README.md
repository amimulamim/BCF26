# Email Sender with CC Support

Send bulk emails via Brevo with CC functionality. Easy to configure and use.

## 📁 Files

- **`config.py`** - **Edit this file** to customize all email settings
- **`send_with_cc.py`** - Main sending script (no need to edit)
- **`recipients.csv`** - Your recipient list
- **`run.sh`** - Quick run script

## ⚙️ Configuration

### 1. Edit `config.py`

**All customizable settings are in `config.py`:**

```python
# Your Brevo API key
BREVO_API_KEY = ""  # Or set as environment variable

# Sender details
FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET CSE Fest 2026"

# Reply-to details
REPLY_TO_EMAIL = "iupc@buetcsefest2026.com"
REPLY_TO_NAME = "IUPC Team"

# Email subject and body
SUBJECT = "BUET CSE Fest 2026 – Important Update"
BODY_TEXT_TEMPLATE = """..."""
DEFAULT_MESSAGE = "Your message here"

# Global CC (sent with EVERY email)
GLOBAL_CC_EMAILS = []  # Example: ["amimul.ehsan2001@gmail.com"]

# Testing
TEST_MODE = False
TEST_TO = "amimul.ehsan2001@gmail.com"

# Rate limiting
SECONDS_BETWEEN_EMAILS = 0.5
```

### 2. Prepare `recipients.csv`

CSV columns:
- **Recipient Email** (required): Main recipient
- **Recipient Name** (required): Name of recipient
- **Team Name** (optional): Team identifier
- **CC Emails** (optional): Comma-separated CC emails for this row
- **Send Now** (required): Set to "YES" to send
- **Mail Sent**: Auto-filled after sending

Example:
```csv
Recipient Email,Recipient Name,Team Name,CC Emails,Send Now,Mail Sent
john@example.com,John Doe,Team A,"jane@example.com, bob@example.com",YES,
```

## 🎯 How to Add CC Recipients

### Option 1: Global CC (sent with EVERY email)

Edit `config.py`:
```python
GLOBAL_CC_EMAILS = ["amimul.ehsan2001@gmail.com", "another@example.com"]
```

### Option 2: Per-Row CC (specific emails only)

Add to CSV's "CC Emails" column:
```csv
Recipient Email,Recipient Name,Team Name,CC Emails,Send Now,Mail Sent
main@example.com,Main Person,Team X,"cc1@example.com, cc2@example.com",YES,
```

### Option 3: Both (Global + Per-Row)

Use both methods - they will be combined (no duplicates).

## 🚀 Usage

### Quick Start

```bash
cd CC_Email_Sender
./run.sh
```

### Manual Run

```bash
cd CC_Email_Sender

# Load API key from .env file (if you have one)
export $(cat ../.env | grep -v '^#' | xargs)

# Run the script
python send_with_cc.py recipients.csv
```

### Custom CSV File

```bash
python send_with_cc.py path/to/your/file.csv
```

## 🧪 Testing

Before sending to real recipients:

1. Set in `config.py`:
   ```python
   TEST_MODE = True
   TEST_TO = "your-test@email.com"
   ```

2. Run the script - all emails go to `TEST_TO` address

3. When ready, set `TEST_MODE = False`

## ✅ Workflow

1. Edit `config.py` - customize settings
2. Update `recipients.csv` - add your recipients
3. Set "Send Now" to "YES" for rows to send
4. Run: `./run.sh` or `python send_with_cc.py recipients.csv`
5. Check output - timestamps are saved in CSV

## 📊 Example: Complete Setup

### config.py
```python
GLOBAL_CC_EMAILS = ["amimul.ehsan2001@gmail.com"]  # Always CC'd
DEFAULT_MESSAGE = "Your slot has been allocated. Check the portal."
SUBJECT = "Slot Allocation - BUET CSE Fest 2026"
```

### recipients.csv
```csv
Recipient Email,Recipient Name,Team Name,CC Emails,Send Now,Mail Sent
team1@example.com,Team Leader 1,Team Alpha,"member1@example.com, member2@example.com",YES,
team2@example.com,Team Leader 2,Team Beta,,YES,
```

**Result:**
- Email 1 sent to: team1@example.com
  - CC: member1@example.com, member2@example.com, amimul.ehsan2001@gmail.com
- Email 2 sent to: team2@example.com
  - CC: amimul.ehsan2001@gmail.com

## 🔒 API Key Setup

### Option 1: In config.py
```python
BREVO_API_KEY = "xkeysib-your-api-key-here"
```

### Option 2: Environment Variable
```bash
export BREVO_API_KEY="xkeysib-your-api-key-here"
python send_with_cc.py recipients.csv
```

### Option 3: .env File (recommended)
Create `../.env` file:
```
BREVO_API_KEY=xkeysib-your-api-key-here
```

Run with:
```bash
./run.sh
```

## ❓ FAQ

**Q: Where are CC emails set?**
A: Two places:
1. `config.py` → `GLOBAL_CC_EMAILS` (for all emails)
2. CSV → `CC Emails` column (per email)

**Q: How to add amimul.ehsan2001@gmail.com to CC?**
A: Edit `config.py`:
```python
GLOBAL_CC_EMAILS = ["amimul.ehsan2001@gmail.com"]
```

**Q: Can I use both global and per-row CC?**
A: Yes! They're combined automatically.

**Q: How to change email content?**
A: Edit `SUBJECT` and `BODY_TEXT_TEMPLATE` in `config.py`

**Q: Rate limit errors?**
A: Increase `SECONDS_BETWEEN_EMAILS` in `config.py`

## 📝 Notes

- Recipients see their own email in "To" field
- CC recipients see all other CC addresses
- No duplicates - if email appears in both global and per-row CC, sent once
- "Mail Sent" column updates automatically with timestamp and message ID
- Only rows with "Send Now" = "YES" are processed
