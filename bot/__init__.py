#!/usr/bin/env python3
# KOYEB FINAL __init__.py - Mirror/Leech/Terabox Bot
# Memory session + user_data + rss_dict fix - COMPLETE SOLUTION

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
from requests import get

# Load environment variables
load_dotenv('config.env', override=True)

# Install uvloop for better performance
install()

# Logging setup
basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[StreamHandler()],
    level=INFO
)
LOGGER = getLogger(__name__)

LOGGER.info("Loading configuration from environment variables...")

# Essential bot variables
BOT_TOKEN = environ.get('BOT_TOKEN', '')
OWNER_ID = int(environ.get('OWNER_ID', '0'))
TELEGRAM_API = int(environ.get('TELEGRAM_API', '0'))
TELEGRAM_HASH = environ.get('TELEGRAM_HASH', '')
DATABASE_URL = environ.get('DATABASE_URL', '')
AUTHORIZED_CHATS = environ.get('AUTHORIZED_CHATS', '')
SUDO_USERS = environ.get('SUDO_USERS', '')

# Koyeb optimized settings
STATUS_UPDATE_INTERVAL = int(environ.get('STATUS_UPDATE_INTERVAL', '10'))
STATUS_LIMIT = int(environ.get('STATUS_LIMIT', '4'))
QUEUE_ALL = int(environ.get('QUEUE_ALL', '2'))
QUEUE_DOWNLOAD = int(environ.get('QUEUE_DOWNLOAD', '1'))
QUEUE_UPLOAD = int(environ.get('QUEUE_UPLOAD', '1'))
LEECH_SPLIT_SIZE = int(environ.get('LEECH_SPLIT_SIZE', '1073741824'))
AS_DOCUMENT = environ.get('AS_DOCUMENT', 'False').lower() == 'true'
DEFAULT_UPLOAD = environ.get('DEFAULT_UPLOAD', 'tg')

# Optional settings
EXCLUDED_EXTENSIONS = environ.get('EXCLUDED_EXTENSIONS', '')
INCOMPLETE_TASK_NOTIFIER = environ.get('INCOMPLETE_TASK_NOTIFIER', 'False').lower() == 'true'
UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'master')
CMD_SUFFIX = environ.get('CMD_SUFFIX', '')

LOGGER.info("Environment variables loaded successfully")

# Data structures for use across modules
user_data = {}
rss_dict = {}

# Validate essential variables
if not BOT_TOKEN:
    LOGGER.error("BOT_TOKEN not found in environment variables!")
    exit(1)
if not OWNER_ID:
    LOGGER.error("OWNER_ID not found in environment variables!")
    exit(1)
if not TELEGRAM_API:
    LOGGER.error("TELEGRAM_API not found in environment variables!")
    exit(1)
if not TELEGRAM_HASH:
    LOGGER.error("TELEGRAM_HASH not found in environment variables!")
    exit(1)

# Bot client instance - MEMORY SESSION FIX
bot = TgClient(
    name=":memory:",
    api_id=TELEGRAM_API,
    api_hash=TELEGRAM_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    parse_mode=enums.ParseMode.HTML,
    in_memory=True
).start()

LOGGER.info("Telegram bot client started successfully")

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
    LOGGER.warning("No database URL provided – bot will operate without database")

LOGGER.info("=== BOT INITIALIZATION COMPLETE ===")
    
