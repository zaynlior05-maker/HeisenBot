# worker_launcher.py — robust polling launcher for telebot
import os
import time
import traceback
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# get token from env (Render provides env vars)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("Missing TELEGRAM_BOT_TOKEN env var. Exiting.")
    raise SystemExit("Missing TELEGRAM_BOT_TOKEN")

# Attempt to import your bot (main.py should register handlers on import)
bot = None
try:
    import main  # noqa: E402
    bot = getattr(main, "bot", None)
    if bot:
        logger.info("Imported bot from main.py")
except Exception:
    logger.info("Could not import bot from main.py (it may raise on import). Trying fallback.")

# Fallback TeleBot if main did not expose bot
if bot is None:
    try:
        import telebot
        bot = telebot.TeleBot(TOKEN)
        logger.warning("Fallback TeleBot created — ensure handlers are registered on import.")
    except Exception:
        logger.error("Failed to create TeleBot fallback:\n%s", traceback.format_exc())
        raise

def start_polling_with_retries():
    backoff = 1
    while True:
        try:
            logger.info("Starting polling (timeout=60, long_polling_timeout=60)...")
            if hasattr(bot, "infinity_polling"):
                bot.infinity_polling(timeout=60, long_polling_timeout=60)
            else:
                bot.polling(non_stop=True, timeout=60, long_polling_timeout=60)
            logger.info("Polling loop exited normally.")
            break
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received, exiting.")
            break
        except Exception:
            logger.error("Exception in polling:\n%s", traceback.format_exc())
            sleep_time = min(backoff, 300)
            logger.info("Sleeping %s seconds before restart...", sleep_time)
            time.sleep(sleep_time)
            backoff = min(backoff * 2, 300)

if __name__ == "__main__":
    logger.info("ENV TELEGRAM_BOT_TOKEN loaded: %s", bool(os.getenv("TELEGRAM_BOT_TOKEN")))
    logger.info("ENV GROUP_CHAT_ID: %s", os.getenv("GROUP_CHAT_ID"))
    start_polling_with_retries()
