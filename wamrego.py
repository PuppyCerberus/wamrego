import sqlite3
import telebot
from Tokens import TOKEN_CERBERUS
cerberus_bot = telebot.TeleBot(TOKEN_CERBERUS)
# Connect to database
conn = sqlite3.connect("PuppyAdventure_Game.db", check_same_thread=False)
# Create a cursor object
c = conn.cursor()
# Create Table
c.execute('CREATE TABLE IF NOT EXISTS player_rego (tg_username TEXT PRIMARY KEY, wam TEXT UNIQUE)')


def db_table_val(tg_username: str, wam: str):
    c.execute('INSERT INTO player_rego (tg_username, wam) VALUES (?, ?)', (tg_username, wam))
    conn.commit()


def check_db(wam: str):
    c.execute('SELECT tg_username FROM player_rego WHERE wam = (?)', (wam,))
    return c.fetchall()


@cerberus_bot.message_handler(commands=['join'])
def join_message(message):
    chat_type = message.chat.type
    wam_input = telebot.util.extract_arguments(message.text)
    username = message.from_user.username
    double_sync_message = " You have had too much beer already"
    sync_message = "  You have successfully join Puppy Adventure🔥🔥🔥"
    try:
        if chat_type != "private" and not check_db(wam_input):
            cerberus_bot.send_message(message.chat.id, "@" + username + sync_message)
            db_table_val(tg_username=username, wam=wam_input)
            print(check_db(wam_input))
        else:
            cerberus_bot.send_message(message.chat.id, "@" + username + double_sync_message)
    except:
        cerberus_bot.send_message(message.chat.id, "@" + username + " dont sync again")


cerberus_bot.polling(none_stop=True)

