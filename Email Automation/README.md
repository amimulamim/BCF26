# Email Automation System

Organized email sending tools for BUET CSE Fest 2026.

## 📁 Project Structure

```
Email Automation/
├── CC_Email_Sender/          ← Send emails with CC recipients
│   ├── config.py            (Edit this for settings)
│   ├── send_with_cc.py      (Main script)
│   ├── recipients.csv       (Your email list)
│   ├── run_campaign.sh              
│   └── README.md           (Full documentation)
│
├── Bulk_Email_Sender/        ← Send bulk campaign emails
│   ├── config.py            (Edit this for settings)
│   ├── send_bulk.py         (Main script)
│   ├── run.sh              (Quick run)
│   └── README.md           (Full documentation)
│
└── .env                      ← API keys (not in git)
```

## 🎯 Which Tool to Use?

### Use **CC_Email_Sender** when:
- You need to send email to one person with others in CC
- Team members should see each other's emails
- You want transparent communication

**Example**: Send slot allocation to team leader, CC all team members

### Use **Bulk_Email_Sender** when:
- Each recipient should receive their own individual email
- No one should see other recipients
- Standard mass email campaigns

**Example**: Send registration confirmation to all teams separately

## 🚀 Quick Start

### CC Email Sender
```bash
cd CC_Email_Sender
./run.sh
```

### Bulk Email Sender
```bash
cd Bulk_Email_Sender
./run.sh
```

## ⚙️ Configuration

Both tools have a `config.py` file with all settings:
- Email subject and body
- Sender and reply-to addresses
- Test mode settings
- Rate limiting

**Just edit `config.py` in the respective folder!**

## 🔑 Setup API Key

Create `.env` file in `Email Automation/` directory:
```bash
BREVO_API_KEY=xkeysib-your-api-key-here
```

Both tools will automatically load it.

## 📚 Documentation

Each folder has its own detailed `README.md`:
- [CC_Email_Sender/README.md](CC_Email_Sender/README.md) - Full guide for CC emails
- [Bulk_Email_Sender/README.md](Bulk_Email_Sender/README.md) - Full guide for bulk emails

## ✨ Features

✅ **Easy Configuration** - All settings in one `config.py` file per tool  
✅ **Test Mode** - Test before sending to real recipients  
✅ **Progress Tracking** - CSV updated after each send  
✅ **Rerun Safe** - Won't duplicate sends  
✅ **Rate Limited** - Configurable delays between emails  
✅ **Well Documented** - Clear README in each folder  

## 🔄 Typical Workflow

1. **Choose tool** (CC or Bulk)
2. **Edit `config.py`** in that folder
3. **Prepare CSV** with recipients
4. **Test first** (enable TEST_MODE)
5. **Send for real** (disable TEST_MODE)
6. **Check results** in CSV "Mail Sent" column

## 💡 Tips

- Always test first with `TEST_MODE = True`
- Keep `.env` file secure (don't commit to git)
- Check CSV after sending for timestamps
- `Bulk_Email_Sender/run.sh` automatically resets before sending

## 📞 Support

Each tool has examples in its README. Check there first!
