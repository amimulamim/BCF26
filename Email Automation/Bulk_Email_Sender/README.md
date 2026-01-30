# Bulk Email Sender

Send bulk emails to teams/participants via Brevo. Simple, configurable, and tracks sent status.

## 📁 Files

- **`config.py`** - **Edit this file** to customize all email settings
- **`send_bulk.py`** - Main sending script (no need to edit)
- **`run.sh`** - Quick run script
- **`process_new_responses.py`** - **Handle incremental form responses** (see below)
- **`sent_teams.json`** - Tracks which teams have already been emailed

---

## 🔄 Handling New Google Form Responses

When the Google Form keeps receiving responses:

### Workflow

1. **Download latest CSV** from Google Sheets (replace `*_new.csv`)

2. **Check for new teams:**
   ```bash
   python process_new_responses.py --check
   ```

3. **Generate JSON for new teams only:**
   ```bash
   python process_new_responses.py --generate
   ```
   This creates `new_team_emails.json` with only unsent teams.

4. **Send emails to new teams** (update `send_dlsprint_start.py` to use `new_team_emails.json`)

5. **Mark as sent after emailing:**
   ```bash
   python process_new_responses.py --mark-sent
   ```

### Initial Setup (First Time)

If you've already sent emails and want to start tracking:
```bash
# Mark all current teams as "already sent"
python process_new_responses.py --mark-all
```

---

## ⚙️ Configuration

### Edit `config.py`

**All customizable settings are in `config.py`:**

```python
# Sender details
FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET CSE Fest 2026"

# Reply-to details (change per campaign)
REPLY_TO_EMAIL = "ctf@buetcsefest2026.com"
REPLY_TO_NAME = "CTF Team"

# Email subject and body
SUBJECT = "BUET CSE Fest 2026 – Update"
BODY_TEXT_TEMPLATE = """..."""
DEFAULT_MESSAGE = "Your message here"

# Testing
TEST_MODE = False
TEST_TO = "amimul.ehsan2001@gmail.com"

# Rate limiting
SECONDS_BETWEEN_EMAILS = 0.3
```

### Prepare Your CSV

Your CSV should have these columns:
- **Email address** (required): Recipient email
- **Team Name** (optional): Team/participant name
- **Send Now** (required): Set to "YES" to send
- **Mail Sent**: Auto-filled after sending

Example CSV (`form_response.csv`):
```csv
Email address,Team Name,Send Now,Mail Sent
team1@example.com,Team Alpha,YES,
team2@example.com,Team Beta,YES,
team3@example.com,Team Gamma,NO,
```

## 🚀 Usage

### Quick Start (Recommended)

```bash
cd Bulk_Email_Sender
./run.sh
```

This will:
1. Reset "Mail Sent" column (clears previous send status)
2. Send emails to all rows with "Send Now" = "YES"

### With Custom CSV File

```bash
./run.sh path/to/your/file.csv
```

### Manual Run (Without Reset)

If you don't want to reset the "Mail Sent" column:

```bash
cd Bulk_Email_Sender

# Load API key from .env
export $(cat ../.env | grep -v '^#' | xargs)

# Run without reset
python send_bulk.py form_response.csv
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

## ✅ Features

- ✅ **Auto Reset**: `run.sh` automatically resets "Mail Sent" column before sending
- ✅ **Smart Filtering**: Only sends to rows with "Send Now" = "YES"
- ✅ **Duplicate Prevention**: Automatically deduplicates email addresses
- ✅ **Progress Tracking**: Saves after each email (safe to interrupt)
- ✅ **Rate Limiting**: Configurable delays between sends
- ✅ **Test Mode**: Test before sending to real recipients

## 📝 Workflow

1. **Edit `config.py`** - Set subject, message, reply-to email
2. **Prepare CSV** - Add recipients, set "Send Now" to "YES"
3. **Test** - Enable TEST_MODE, verify email looks good
4. **Send** - Disable TEST_MODE, run `./run.sh`
5. **Track** - Check "Mail Sent" column for timestamps

## 🔄 Resending

**Option 1: Full reset (all rows)**
```bash
./run.sh  # Automatically resets all rows and resends
```

**Option 2: Selective reset**
1. Manually clear "Mail Sent" column for specific rows in CSV
2. Keep "Send Now" as "YES"
3. Run: `python send_bulk.py form_response.csv` (without reset)

## 📊 Example

### Before Running:
```csv
Email address,Team Name,Send Now,Mail Sent
team1@example.com,Team Alpha,YES,
team2@example.com,Team Beta,YES,
team3@example.com,Team Gamma,NO,
```

### After Running:
```csv
Email address,Team Name,Send Now,Mail Sent
team1@example.com,Team Alpha,YES,2026-01-16T11:30:00+06:00 | <msg-id-123>
team2@example.com,Team Beta,YES,2026-01-16T11:30:01+06:00 | <msg-id-456>
team3@example.com,Team Gamma,NO,
```

## 🔒 API Key Setup

Same as CC_Email_Sender - use `.env` file:
```
BREVO_API_KEY=xkeysib-your-api-key-here
```

## ❓ Common Tasks

**Change email content?**
→ Edit `SUBJECT`, `BODY_TEXT_TEMPLATE`, `DEFAULT_MESSAGE` in `config.py`

**Change reply-to address?**
→ Edit `REPLY_TO_EMAIL` and `REPLY_TO_NAME` in `config.py`

**Send faster/slower?**
→ Adjust `SECONDS_BETWEEN_EMAILS` in `config.py`

**Test first?**
→ Set `TEST_MODE = True` in `config.py`
