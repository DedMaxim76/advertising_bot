from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

MAIN_CHANNEL_ID = env.str("MAIN_CHANNEL_ID")
MAIN_CHANNEL_URL = env.str("MAIN_CHANNEL_URL")
MAIN_CHAT_ID = env.str("MAIN_CHAT_ID")
MAIN_CHAT_URL = env.str("MAIN_CHAT_URL")

CURRENT_GAME_ID = 0

ADMIN_BALANCE = 0
BALANCE_LIMIT = 1000
INVITER_CODE = "877666567"

QIWI_TOKEN = env.str("qiwi")
WALLET_QIWI = env.str("wallet")
QIWI_PUBKEY = env.str("qiwi_pubkey")

db_host = IP

PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
DATABASE = env.str("DATABASE")

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{DATABASE}"
