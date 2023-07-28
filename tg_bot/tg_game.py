from telebot.async_telebot import AsyncTeleBot, types
from random import randrange
from time import sleep
import asyncio
import psycopg2
import tracemalloc


bot = AsyncTeleBot("5710299504:AAFoermLvSR-MUNcLADs2FuyWCDxkAiJh4o")

conn = psycopg2.connect(host="localhost", database="tg", user="serojisahakyan")
cursor = conn.cursor()

# Handle '/start', '/help', '/stop', '/gameResults', '/deleteAccount' commands
@bot.message_handler(commands=["help", "start", "stop", "gameResults", "deleteAccount"])
async def send_welcome(message):
    # Function to handle '/start' command
    if message.text == "/start":
        keyboard = types.ReplyKeyboardMarkup(
            row_width=3, resize_keyboard=False, one_time_keyboard=False
        )
        help = types.KeyboardButton(text="/help")
        stop = types.KeyboardButton(text="/stop")
        paper = types.KeyboardButton(text="✋")
        scissors = types.KeyboardButton(text="✌️")
        fireplace = types.KeyboardButton(text="👊")
        game_results = types.KeyboardButton(text="/gameResults")
        deleteAccount = types.KeyboardButton(text="/deleteAccount")
        keyboard.add(paper, scissors, fireplace, help, game_results, deleteAccount, stop)
        await bot.send_message(
            message.chat.id,
            "Добро пожаловать в игру камень ножницы бумага✌️👊🖐️",
            reply_markup=keyboard
            )
    # Function to handle '/stop' command
    elif message.text == "/stop":
        keyboard = types.ReplyKeyboardMarkup(
            row_width=3, resize_keyboard=False, one_time_keyboard=False
        )
        start = types.KeyboardButton(text="/start")
        keyboard.add(start)
        await bot.send_message(
            message.chat.id,
            "игра астановленая",
            reply_markup=keyboard, 
        )
    # Function to handle '/deleteAccount' command
    elif message.text == "/deleteAccount":
        markup = types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton("yes", callback_data="del_yes")
        no = types.InlineKeyboardButton("no", callback_data="del_no")
        markup.add(yes, no)
        await bot.send_message(
            message.chat.id,
            text="Are you sure you want to delete the game account",
            reply_markup=markup,
        )
    # Function to handle '/gameResults' command
    elif message.text == "/gameResults":
        await bot.send_message(message.chat.id, f"me bot\n{me_result()}    {bot_result()}")
    # Function to handle '/help' command
    elif message.text == "/help":
        await bot.send_message(message.chat.id, "/start - Help start the game\n/stop - Help end the game\n/gameResults - Help calculate the game results\n/deleteAccount - Help clear the results of the previous game")

#  Generates a random response sticker and sends it with a custom keyboard
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    lst = ["👊", "✋", "✌️"]
    keyboard = types.ReplyKeyboardMarkup(
        row_width=3, resize_keyboard=False, one_time_keyboard=False
    )
    help = types.KeyboardButton(text="/help")
    paper = types.KeyboardButton(text="✋")
    scissors = types.KeyboardButton(text="✌️")
    fireplace = types.KeyboardButton(text="👊")
    game_results = types.KeyboardButton(text="/gameResults")
    deleteAccount = types.KeyboardButton(text="/deleteAccount")
    stop = types.KeyboardButton(text="/stop")
    keyboard.add(paper, scissors, fireplace, help, game_results, deleteAccount, stop)
    sleep(0.05)
    bot_message = lst[randrange(3)]
    await bot.send_message(message.chat.id, bot_message, reply_markup=keyboard)
    await bot.send_message(message.chat.id, f"{comparisons_message(message.text, bot_message)}", reply_markup=keyboard)

# Here the button click is being processed
@bot.callback_query_handler(func=lambda call: True)
async def callback(call):
    if call.message:
        if call.data == "del_yes":
            cursor.execute("TRUNCATE TABLE tg_game")
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text="Аll deleted successfully",
            )
        if call.data == "del_no":
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text="The process is stopped",
            )

# Function to compare the player's and bot's choices and determine the result
def comparisons_message(your_message, message_bot):
    if your_message == message_bot:
        return "НИЧЬЯ"
    elif your_message == "✋" and message_bot == "✌️":
        return bot_won()
    elif your_message == "✋" and message_bot == "👊":
        return you_win()
    elif your_message == "👊" and message_bot == "✋":
        return bot_won()
    elif your_message == "👊" and message_bot == "✌️":
        return you_win()
    elif your_message == "✌️" and message_bot == "👊":
        return bot_won()
    elif your_message == "✌️" and message_bot == "✋":
        return you_win()

# Function to handle bot's victory
def bot_won():
    cursor.execute("INSERT INTO tg_game (bot) VALUES (1)")
    conn.commit()
    return "ВЫ ПРИГЛАСИЛИ"

# Function to handle player's victory
def you_win():
    cursor.execute("INSERT INTO tg_game (me) VALUES (1)")
    conn.commit()
    return "ВЫ ПОБЕДИЛИ"

# Function to calculate the player's game result
def me_result():
    real_result = 0
    cursor.execute("SELECT me FROM tg_game")
    result = cursor.fetchall()
    for i in result:
        if i == (1,):
            real_result += 1
    return real_result

# Function to calculate the bot's game result
def bot_result():
    real_result = 0
    cursor.execute("SELECT bot FROM tg_game")
    result = cursor.fetchall()
    for i in result:
        if i == (1,):
            real_result += 1
    return real_result

# Starts the bot's polling loop to listen for incoming messages
asyncio.run(bot.polling(non_stop=True))
