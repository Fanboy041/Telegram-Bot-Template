import telebot, logging
import os
import importlib
# from UFO import main
from telebot.types import ChatMemberUpdated
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# load the .env file
load_dotenv()


# Draw UFO in console
# main()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

try:
    # Logging configuration 
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # RotatingFileHandler
    max_log_size_mb = 5  # Set your desired maximum log size in megabytes
    file_handler = RotatingFileHandler('./bot.log', maxBytes=max_log_size_mb * 1024 * 1024, backupCount=1)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)




    commands_dir = os.path.join(os.path.dirname(__file__), 'Commands')
    commands = {}

    for foldername in os.listdir(commands_dir):
        if foldername.endswith('.py') and foldername != '__init__.py':

            command_name = os.path.splitext(foldername)[0]
            command = importlib.import_module(f'Commands.{command_name}')
            commands[command_name] = command


    features_dir = os.path.join(os.path.dirname(__file__), 'Features')
    features = {}

    for foldername in os.listdir(features_dir):
        if foldername.endswith('.py') and foldername != '__init__.py':

            feature_name = os.path.splitext(foldername)[0]
            feature = importlib.import_module(f'Features.{feature_name}')
            features[feature_name] = feature


    logging.info("Main script runs successfully, Bot is working") 

    # New joined chat member handler
    @bot.message_handler(content_types=['new_chat_members'])
    def handle_add_group_chat_id(message):
        if 'addGroupChatId' in features:
            features['addGroupChatId'].add_group_chat_id(message, bot)

    # Left chat member handler
    @bot.message_handler(content_types=['left_chat_member'])
    def handle_add_group_chat_id(message):
        if 'deleteGroupChatId' in features:
            features['deleteGroupChatId'].delete_group_chat_id(message, bot)

    # New channel add handler
    @bot.my_chat_member_handler()
    def handle_add_channel_chat_id(chat_member_update: ChatMemberUpdated):
        if 'addChannelChatId' in features:
            features['addChannelChatId'].add_channel_chat_id(chat_member_update, bot)

    # Start command
    @bot.message_handler(commands=['start'])
    def handle_start_command(message):
        if 'startCommand' in commands:
            commands['startCommand'].send_welcome(message, bot)

    # Settings command
    @bot.message_handler(commands=['settings'])
    def handle_settings_command(message):
        if 'settingsCommand' in commands:
            commands['settingsCommand'].settings_command(message, bot)

    # Handle the urls that sent in groups
    @bot.message_handler(content_types=['text'])
    def handle_antispam_group(message):        
        if 'antispamGroup' in features:
            features['antispamGroup'].antispam_group(message, bot)


    
    bot.infinity_polling()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")