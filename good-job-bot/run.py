#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random
import re

from telegram import ForceReply, Update
from dotenv import dotenv_values
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def is_success_message(message: str) -> bool:
    """Check if the message is a success message."""
    return any(
        success in message.lower()
        for success in [
            "done",
            "fertig",
            "success",
            "erledigt",
            "completed",
            "geschaut",
            "✔️",
            "✅",
            "☑️",
            "checked in",
        ]
    )


def get_success_message() -> str:
    """Get a random success message."""
    return random.choice(
        [
            "🎉",
            "🎊",
            "🎈",
            "🎁",
            "🎆",
            "🎇",
            "💪",
            "❤️",
            "⭐️",
            "✨",
            "🌟",
            "💫",
            "🌠",
            "🌈",
            "🔥",
            "Proud of you!",
            "You did it!",
            "You got a step closer to your ideal self!",
            "Improving, I see!",
            "You are doing great!",
            "Wow, look at you!",
            "You are a star!",
            "I knew you could do it!",
            "I'm glad I could help!",
            "You are amazing!",
            "You are awesome!",
            "You are incredible!",
            "You are inspiring!",
            "You are wonderful!",
            "You are simply the best!",
            "You should be proud of yourself!",
            "You are one of a kind!",
        ]
    )


async def good_job(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Tell the user they did a good job."""
    is_username = update.message.from_user.username
    should_username = get_const("USERNAME")
    if is_username != should_username:
        return

    if not is_success_message(update.message.text):
        return

    emoji = get_success_message()
    await update.message.reply_text(emoji)


def get_const(key: str) -> str:
    """Get a constant from the .env file."""
    config = dotenv_values(".env")
    return config[key]


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    token = get_const("TELEGRAM_TOKEN")
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, good_job))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
