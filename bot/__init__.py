#!/usr/bin/env python3
import asyncio
from asyncio.subprocess import PIPE
from threading import Thread
from time import time
from functools import partial
from os import environ, path as ospath, remove as osremove
from subprocess import run as srun, check_output
from logging import getLogger, StreamHandler, basicConfig, INFO
from dotenv import load_dotenv
from aiofiles.os import path as aiopath, remove as aioremove, rename as aiorename, makedirs
from aioshutil import rmtree as aiormtree
from pyrogram import Client as TgClient, enums
from requests import get

# Load environment variables
load_dotenv('config.env', override=True)

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

# Settings
STATUS_UPDATE_INTERVAL = int(environ.get('STATUS_UPDATE_INTERVAL', '10'))
STATUS_LIMIT = int(environ.get('STATUS_LIMIT', '4'))
QUEUE_ALL = int(environ.get('QUEUE_ALL', '2'))
QUEUE_DOWNLOAD = int(environ.get('QUEUE_DOWNLOAD', '1'))
QUEUE_UPLOAD = int(environ.get('QUEUE_UPLOAD', '1'))
LEECH_SPLIT_SIZE = int(environ.get('LEECH_SPLIT_SIZE', '1073741824'))
AS_DOCUMENT = environ.get('AS_DOCUMENT', 'False').lower() == 'true'
DEFAULT_UPLOAD = environ.get('DEFAULT_UPLOAD', 'tg')
EXCLUDED_EXTENSIONS = environ.get('EXCLUDED_EXTENSIONS', '')
INCOMPLETE_TASK_NOTIFIER = environ.get('INCOMPLETE_TASK_NOTIFIER', 'False').lower() == 'true'
UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'master')
CMD_SUFFIX = environ.get('CMD_SUFFIX', '')

LOGGER.info("Environment variables loaded successfully")

# Shared data structures
user_data = {}
rss_dict = {}
qbit_options = {}
bot_loop = None
status_dict = {}

# Validate essential variables
if not BOT_TOKEN or not OWNER_ID or not TELEGRAM_API or not TELEGRAM_HASH:
    LOGGER.error("Essential variables not set!")
    exit(1)

# Initialize bot client
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

# Initialize database if URL provided
if DATABASE_URL:
    from .helper.ext_utils.db_handler import DbManager
    DbManager()
    LOGGER.info("Connected to database successfully")

# Essential bot commands and filters
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker

# Core modules
from .modules import authorize, bot_settings, cancel_mirror, mirror_leech, status, users_settings

LOGGER.info("=== KOYEB MIRROR/LEECH BOT READY ===")
