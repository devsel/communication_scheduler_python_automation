import json
import logging
import os

import pywhatkit
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "scheduler.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

load_dotenv(os.path.join(BASE_DIR, ".env"))

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
slack_client = WebClient(token=SLACK_BOT_TOKEN) if SLACK_BOT_TOKEN else None


def load_config():
    """Load scheduled messages from config.json."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def send_whatsapp(phone, message):
    """Send a WhatsApp message through WhatsApp Web using PyWhatKit."""
    logging.info("Sending WhatsApp message to %s", phone)

    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=15,
            tab_close=True,
        )
        logging.info("WhatsApp message sent to %s", phone)
        print(f"✅ WhatsApp message sent to {phone}")
    except Exception as exc:
        logging.exception("WhatsApp error: %s", exc)
        print(f"❌ WhatsApp error: {exc}")


def send_slack(channel, message):
    """Send a message to a Slack channel using the Slack Web API."""
    if not slack_client:
        logging.error("SLACK_BOT_TOKEN is not configured.")
        print("❌ Slack token is not configured.")
        return

    logging.info("Sending Slack message to %s", channel)

    try:
        response = slack_client.chat_postMessage(
            channel=channel,
            text=message,
        )

        if response.get("ok"):
            logging.info("Slack message sent to %s", channel)
            print(f"✅ Slack message sent to {channel}")
    except SlackApiError as exc:
        error = exc.response.get("error", "unknown_error")
        logging.exception("Slack API error: %s", error)
        print(f"❌ Slack API error: {error}")


def send_message(job):
    """Route a scheduled job to the correct communication service."""
    message_type = job["type"]

    if message_type == "whatsapp":
        send_whatsapp(job["phone"], job["message"])
    elif message_type == "slack":
        send_slack(job["channel"], job["message"])
    else:
        logging.error("Unknown message type: %s", message_type)
        print(f"❌ Unknown message type: {message_type}")


def schedule_job(scheduler, job):
    """Create an APScheduler cron job from one config entry."""
    hour, minute = map(int, job["time"].split(":"))
    job_id = job.get("name", "scheduled-message").lower().replace(" ", "-")

    if "date" in job:
        month, day = map(int, job["date"].split("-"))

        trigger = CronTrigger(
            month=month,
            day=day,
            hour=hour,
            minute=minute,
        )
        description = f"yearly on {job['date']} at {job['time']}"
    else:
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
        )
        description = f"daily at {job['time']}"

    scheduler.add_job(
        send_message,
        trigger=trigger,
        args=[job],
        id=job_id,
        replace_existing=True,
    )

    print(f"⏰ {job['name']}: {description}")


def main():
    print("=" * 60)
    print("       PYTHON COMMUNICATION SCHEDULER")
    print("=" * 60)

    try:
        config = load_config()
    except FileNotFoundError:
        print("❌ config.json was not found.")
        return
    except json.JSONDecodeError as exc:
        print(f"❌ Invalid JSON in config.json: {exc}")
        return

    messages = config.get("messages", [])
    if not messages:
        print("⚠️ No messages found in config.json.")
        return

    scheduler = BlockingScheduler()

    for job in messages:
        schedule_job(scheduler, job)

    print("\n🚀 Scheduler is running.")
    print("Press CTRL+C to stop.\n")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Scheduler stopped.")
        logging.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
