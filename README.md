# 💬 Python Communication Scheduler

A beginner-friendly Python automation project that schedules WhatsApp and Slack messages.

The project is designed as a YouTube tutorial / portfolio project and demonstrates:

- Python scheduling with APScheduler
- WhatsApp Web automation with PyWhatKit
- Slack messages with the Slack SDK
- Environment variables for secrets
- JSON-based message configuration
- Logging
- Git/GitHub project organization

## Features

- Daily WhatsApp reminders
- Daily Slack team messages
- Yearly birthday messages
- Central `config.json` configuration
- `.env` secret management
- Activity logs
- Easy extension for additional message types

## Project structure

```text
communication_scheduler/
├── src/
│   └── scheduler.py
├── logs/
├── data/
├── config.json
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Slack

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then put your Slack bot token in `.env`:

```env
SLACK_BOT_TOKEN=xoxb-your-real-token
```

Give the Slack app only the permissions it needs and invite the bot to the target channel.

Do not commit `.env` to GitHub.

## 4. Configure messages

Edit `config.json`.

Daily job:

```json
{
  "type": "slack",
  "name": "Daily Team Reminder",
  "channel": "#general",
  "message": "Good morning team!",
  "time": "09:00"
}
```

WhatsApp job:

```json
{
  "type": "whatsapp",
  "name": "Morning Reminder",
  "phone": "+33123456789",
  "message": "Good morning!",
  "time": "09:05"
}
```

Yearly birthday job:

```json
{
  "type": "whatsapp",
  "name": "Birthday Wish",
  "phone": "+33123456789",
  "message": "Happy Birthday!",
  "time": "09:10",
  "date": "08-20"
}
```

Use international phone-number format for WhatsApp.

## 5. Run the scheduler

From the project root:

```bash
python src/scheduler.py
```

The program stays running and waits for scheduled times.

Press `Ctrl+C` to stop it.

## Important WhatsApp note

PyWhatKit works through WhatsApp Web. The computer running the script should have a WhatsApp Web session available. Browser automation can be affected by changes to WhatsApp Web.

Only send messages to people or groups where you have permission to automate communication, and avoid spam.

## Git workflow

This project is intended to use a dedicated branch named:

```text
python-automation
```

Create it with:

```bash
git checkout -b python-automation
```

Then:

```bash
git add .
git commit -m "Add Python communication scheduler"
git push -u origin python-automation
```

## Suggested YouTube improvements

Future episodes can add:

- CustomTkinter graphical interface
- SQLite message history
- Email notifications
- Retry handling
- Scheduled one-time messages
- A dashboard showing sent messages
- Multiple Slack channels
- Better validation and tests

## License

This project is provided for educational purposes. Add a license appropriate for how you intend to publish and reuse the code.
