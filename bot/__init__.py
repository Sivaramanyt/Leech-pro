#!/usr/bin/env python3
# KOYEB COMPATIBLE bot/__init__.py - Mirror/Leech/Terabox Bot
# Maintains all essential exports while removing problematic imports

from aiofiles.os import path as aiopath, remove as aioremove, rename as aiorename, makedirs
from aioshutil import rmtree as aiormtree
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep
from asyncio.subprocess import PIPE
from dotenv import load_dotenv
from functools import partial
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig, ERROR, WARNING
from os import environ, getcwd, path as ospath, remove as osremove
from pyrogram import Client as TgClient, enums
from subprocess import run as srun, check_output
from threading import Thread
from time import time
from uvloop import install

# Load environment variables
load_dotenv('config.env', override=True)

# Install uvloop for better performance
install()

# Logging setup
basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[StreamHandler()], level=INFO)
LOGGER = getLogger(__name__)

# Bot configuration - Essential exports
CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL')
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = get(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.py', 'wb+') as f:
                f.write(res.content)
        else:
            LOGGER.error(f"Failed to download config.py {res.status_code}")
    except Exception as e:
        LOGGER.error(f"CONFIG_FILE_URL: {e}")
except:
    pass

# Config import
try:
    from .config import *
    LOGGER.info("Config loaded from config.py")
except ImportError:
    from bot.config import *
    LOGGER.info("Config loaded from bot.config")
except Exception as e:
    LOGGER.info("Config module not found, loading from environment variables...")

# Essential bot variables - MUST BE EXPORTED
BOT_TOKEN = environ.get('BOT_TOKEN', '')
OWNER_ID = int(environ.get('OWNER_ID', '0'))
TELEGRAM_API = int(environ.get('TELEGRAM_API', '0'))
TELEGRAM_HASH = environ.get('TELEGRAM_HASH', '')
DATABASE_URL = environ.get('DATABASE_URL', '')
AUTHORIZED_CHATS = environ.get('AUTHORIZED_CHATS', '')
SUDO_USERS = environ.get('SUDO_USERS', '')

# Bot client instance
bot = TgClient(
    name="bot",
    api_id=TELEGRAM_API,
    api_hash=TELEGRAM_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    parse_mode=enums.ParseMode.HTML
).start()

# Essential imports for mirror/leech functionality
from .helper.ext_utils.db_handler import DbManager
from .helper.ext_utils.bot_utils import sync_to_async, new_task
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker

# Import only essential modules (removed problematic imports)
from .modules import authorize, bot_settings, cancel_mirror, mirror_leech, status, users_settings

# Essential bot info
VERSION = "Koyeb Optimized v1.0"
LOGGER.info(f"Bot Version: {VERSION}")
LOGGER.info("Koyeb Optimized Mirror/Leech Bot Started Successfully!")

# Database initialization
if DATABASE_URL:
    DbManager()
    LOGGER.info("Database connected successfully")
else:
    LOGGER.warning("No database URL provided")
    
