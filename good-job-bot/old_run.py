#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import dotenv_values


async def hello(update: Update, context: "ContextTypes.DEFAULT_TYPE") -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


if __name__ == "__main__":
    config = dotenv_values(".env")
    token = config["TELEGRAM_TOKEN"]

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.run_polling()
