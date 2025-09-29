#!/usr/bin/env python3
import uuid, time, logging
from os import environ
from dotenv import load_dotenv
from pyrogram import Client as TgClient, enums

# -------- 1. Load .env --------
load_dotenv("config.env", override=True)

# -------- 2. Logging --------
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
LOGGER = logging.getLogger("MLTB")

# -------- 3. Mandatory ENV --------
BOT_TOKEN     = environ.get("BOT_TOKEN", "")
OWNER_ID      = int(environ.get("OWNER_ID", "0"))
TELEGRAM_API  = int(environ.get("TELEGRAM_API", "0"))
TELEGRAM_HASH = environ.get("TELEGRAM_HASH", "")

if not all([BOT_TOKEN, OWNER_ID, TELEGRAM_API, TELEGRAM_HASH]):
    LOGGER.error("❌ Missing required environment variables!")
    raise SystemExit

# -------- 4. Shared Dicts --------
user_data   = {}
rss_dict    = {}
qbit_options= {}
status_dict = {}
bot_loop    = None

# -------- 5. Unique session filename (avoids sqlite lock) --------
session_name = f"koyeb_{int(time.time())}_{uuid.uuid4().hex[:6]}"

# -------- 6. Start Bot --------
LOGGER.info("🚀 Starting Telegram bot …")
bot = TgClient(
    name=session_name,          # unique sqlite file
    api_id=TELEGRAM_API,
    api_hash=TELEGRAM_HASH,
    bot_token=BOT_TOKEN,
    workers=100,
    parse_mode=enums.ParseMode.HTML
).start()
LOGGER.info("✅ Bot connected to Telegram")

# -------- 7. Optional: connect MongoDB --------
DATABASE_URL = environ.get("DATABASE_URL", "")
if DATABASE_URL:
    from .helper.ext_utils.db_handler import DbManager
    DbManager()
    LOGGER.info("✅ Connected to MongoDB")

# -------- 8. Import core modules --------
from .helper.telegram_helper.bot_commands   import BotCommands
from .helper.telegram_helper.message_utils  import sendMessage, editMessage, deleteMessage
from .helper.telegram_helper.filters        import CustomFilters
from .helper.telegram_helper.button_build   import ButtonMaker
from .modules import authorize, bot_settings, cancel_mirror, mirror_leech, status, users_settings

LOGGER.info("🎉 Mirror/Leech/Terabox bot is LIVE!")
    
