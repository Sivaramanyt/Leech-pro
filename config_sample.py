# KOYEB OPTIMIZED CONFIG - MIRROR/LEECH/TERABOX BOT
# Simplified configuration for 512MB RAM deployment

from logging import ERROR

# ===== REQUIRED FIELDS =====
BOT_TOKEN = ""
OWNER_ID = 
TELEGRAM_API = 
TELEGRAM_HASH = ""

# ===== DATABASE =====
DATABASE_URL = ""

# ===== BASIC SETTINGS =====
AUTHORIZED_CHATS = ""
SUDO_USERS = ""
STATUS_UPDATE_INTERVAL = 10
STATUS_LIMIT = 4

# ===== KOYEB RAM OPTIMIZED LIMITS =====
QUEUE_ALL = 2
QUEUE_DOWNLOAD = 1  
QUEUE_UPLOAD = 1
TORRENT_TIMEOUT = 300

# ===== LEECH SETTINGS (Koyeb Optimized) =====
LEECH_SPLIT_SIZE = 1073741824  # 1GB for 512MB RAM
AS_DOCUMENT = False
LEECH_DUMP_CHAT = ""
LEECH_FILENAME_PREFIX = ""
EQUAL_SPLITS = False
MEDIA_GROUP = False

# ===== UPLOAD SETTINGS =====
DEFAULT_UPLOAD = "tg"  # Upload to Telegram by default
GDRIVE_ID = ""
RCLONE_PATH = ""
IS_TEAM_DRIVE = False
STOP_DUPLICATE = False

# ===== OPTIONAL SETTINGS =====
EXCLUDED_EXTENSIONS = ""
INCOMPLETE_TASK_NOTIFIER = False
UPSTREAM_REPO = ""
UPSTREAM_BRANCH = "master"
CMD_SUFFIX = ""

# ===== LOGGING =====
LOG_LEVEL = ERROR

# ===== REMOVED FOR KOYEB OPTIMIZATION =====
# All JDownloader, Sabnzbd, RSS, Search, FFmpeg variables removed
# This reduces RAM usage by ~400MB and eliminates unused dependencies
