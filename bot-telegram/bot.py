"""
Telegram Bot Example - GitHub Portfolio Project
Created by: [Your Name]
Description: A feature-rich Telegram bot using python-telegram-bot library
"""

import os
import logging
from typing import Final
from datetime import datetime
import json
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Load environment variables
load_dotenv()

# Configuration
TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID: Final = os.getenv('ADMIN_ID', '')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Data storage (in production, use a database)
user_data = {}

# ===================== Helper Functions =====================

def save_user_data(user_id: int, username: str, action: str):
    """Save user activity to a log file"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'username': username,
        'action': action
    }
    
    try:
        with open('bot_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        logger.error(f"Error saving log: {e}")

# ===================== Command Handlers =====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    # Save user activity
    save_user_data(user_id, username, 'start_command')
    
    welcome_message = f"""
    🤖 Welcome {user.first_name}!

    I'm a sample Telegram bot created for GitHub portfolio.

    🚀 Available Commands:
    /start - Start the bot
    /help - Show help message
    /about - About this project
    /info - Get user info
    /stats - Get bot statistics
    /contact - Contact information

    📝 Try sending me a message or use the buttons below!
    """
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("📊 GitHub", url="https://github.com/yourusername"),
            InlineKeyboardButton("📁 View Source", url="https://github.com/yourusername/telegram-bot-sample")
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data='about'),
            InlineKeyboardButton("🛠️ Commands", callback_data='commands')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    logger.info(f"User {username} started the bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command"""
    help_text = """
    📚 **Help Guide**

    **Basic Commands:**
    • `/start` - Start the bot
    • `/help` - Show this help message
    • `/about` - About this project
    • `/info` - Get your user information
    • `/stats` - Get bot statistics
    • `/contact` - Contact the developer

    **Features:**
    • Echo messages
    • User information
    • GitHub integration
    • Button interactions
    • Activity logging

    **Source Code:**
    This bot is open-source! Check out the code on [GitHub](https://github.com/yourusername/telegram-bot-sample)
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')
    save_user_data(update.effective_user.id, update.effective_user.username, 'help_command')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /about command"""
    about_text = """
    🤖 **Telegram Bot Sample - GitHub Portfolio**

    **Description:**
    This is a sample Telegram bot created with python-telegram-bot library.
    It demonstrates clean code structure, error handling, and various features.

    **Tech Stack:**
    • Python 3.9+
    • python-telegram-bot 20.0+
    • Environment variables
    • JSON logging

    **Features Included:**
    ✅ Command handlers
    ✅ Message echo
    ✅ Inline keyboards
    ✅ Callback queries
    ✅ User data handling
    ✅ Error handling
    ✅ Activity logging

    **GitHub:** https://github.com/yourusername
    """
    
    await update.message.reply_text(about_text, parse_mode='Markdown')
    save_user_data(update.effective_user.id, update.effective_user.username, 'about_command')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /info command - Get user information"""
    user = update.effective_user
    
    user_info = f"""
    👤 **User Information**

    **ID:** `{user.id}`
    **Name:** {user.first_name}
    **Username:** @{user.username if user.username else 'N/A'}
    **Language:** {user.language_code if user.language_code else 'N/A'}
    **Profile:** [Link](tg://user?id={user.id})

    **Bot Join Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    await update.message.reply_text(user_info, parse_mode='Markdown')
    save_user_data(user.id, user.username, 'info_command')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /stats command"""
    user = update.effective_user
    
    # Check if admin
    if str(user.id) != ADMIN_ID:
        await update.message.reply_text("⚠️ This command is for admin only.")
        return
    
    # Simple stats (in production, use database)
    stats_text = f"""
    📊 **Bot Statistics**

    **Total Users:** {len(user_data)}
    **Uptime:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    **Admin:** {user.first_name}
    
    *Note: These are sample statistics.*
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /contact command"""
    contact_text = """
    📞 **Contact Information**

    **Developer:** [Your Name]
    **GitHub:** [yourusername](https://github.com/yourusername)
    **Email:** your.email@example.com
    **Portfolio:** https://yourportfolio.com

    **Project Repository:**
    https://github.com/yourusername/telegram-bot-sample

    Feel free to check out my other projects on GitHub!
    """
    
    keyboard = [
        [InlineKeyboardButton("🌐 GitHub Profile", url="https://github.com/yourusername")],
        [InlineKeyboardButton("📁 View Source Code", url="https://github.com/yourusername/telegram-bot-sample")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(contact_text, parse_mode='Markdown', reply_markup=reply_markup)

# ===================== Message Handlers =====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages"""
    user = update.effective_user
    message_text = update.message.text
    
    # Save user activity
    save_user_data(user.id, user.username, f'message: {message_text[:20]}...')
    
    # Echo the message with some processing
    response = f"📝 You said: {message_text}\n\n"
    response += f"📊 Message Info:\n"
    response += f"• Length: {len(message_text)} characters\n"
    response += f"• Words: {len(message_text.split())}\n"
    response += f"• User: {user.first_name}"
    
    await update.message.reply_text(response)
    logger.info(f"Echoed message from {user.username}: {message_text}")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'about':
        await query.edit_message_text(
            text="ℹ️ **About This Bot**\n\nThis is a sample bot created for GitHub portfolio. "
                 "It demonstrates various Telegram Bot API features and clean Python code structure.",
            parse_mode='Markdown'
        )
    elif query.data == 'commands':
        await query.edit_message_text(
            text="🛠️ **Available Commands**\n\n"
                 "/start - Start the bot\n"
                 "/help - Show help\n"
                 "/about - About project\n"
                 "/info - User info\n"
                 "/stats - Statistics\n"
                 "/contact - Contact info",
            parse_mode='Markdown'
        )
    
    save_user_data(update.effective_user.id, update.effective_user.username, f'callback: {query.data}')

# ===================== Error Handler =====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    try:
        # Notify admin about error
        if ADMIN_ID:
            error_msg = f"⚠️ Bot Error:\n{context.error}"
            await context.bot.send_message(chat_id=ADMIN_ID, text=error_msg)
    except:
        pass

# ===================== Main Function =====================

def main():
    """Start the bot"""
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        print("Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("contact", contact_command))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("🤖 Bot is starting...")
    print(f"👤 Admin ID: {ADMIN_ID if ADMIN_ID else 'Not set'}")
    print("📝 Logs are being saved to bot_log.json")
    print("🚀 Press Ctrl+C to stop the bot")
    
    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
