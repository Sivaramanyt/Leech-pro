#!/usr/bin/env python3
# KOYEB OPTIMIZED bot/__init__.py - Mirror/Leech/Terabox Bot
# Cleaned version with only essential imports for 512MB RAM

import asyncio
import signal
import time
from datetime import datetime
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig, ERROR, WARNING
from os import remove as osremove, path as ospath, environ
from pyrogram import idle
from sys import exit as sysexit
from threading import Thread

# Essential imports only
from .helper.ext_utils.db_handler import DbManager
from .helper.ext_utils.bot_utils import sync_to_async, new_task
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker
from .helper.mirror_leech_utils.status_utils.status_utils import get_readable_file_size, get_readable_time
from .modules import authorize, bot_settings, cancel_mirror, mirror_leech, status, users_settings

# Logging setup
LOGGER = getLogger(__name__)

# Bot version info
VERSION = "Koyeb Optimized v1.0"

class SignalHandler:
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        LOGGER.info(f"Received signal {signum}. Shutting down gracefully...")
        sysexit(0)

def main():
    """Main function to start the bot"""
    try:
        # Initialize signal handler
        signal_handler = SignalHandler()
        
        # Start the bot
        LOGGER.info("Starting Koyeb Optimized Mirror/Leech Bot...")
        LOGGER.info(f"Version: {VERSION}")
        
        # Keep the bot running
        idle()
        
    except Exception as e:
        LOGGER.error(f"Error in main: {e}")
        sysexit(1)

if __name__ == "__main__":
    main()
        
