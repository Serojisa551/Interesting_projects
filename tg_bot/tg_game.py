from telebot.async_telebot import AsyncTeleBot, types
from random import randrange
from time import sleep
import asyncio
bot = AsyncTeleBot("5710299504:AAFoermLvSR-MUNcLADs2FuyWCDxkAiJh4o")

# TODO(
# Handle '/start' and '/help' and '/stop'
@bot.message_handler(commands=["help", "start", "stop"])
async def send_welcome(message):
    if message.text == "/start":
        keyboard = types.ReplyKeyboardMarkup(
            row_width=3, resize_keyboard=False, one_time_keyboard=False
        )
        stop = types.KeyboardButton(text="/stop")
        paper = types.KeyboardButton(text="✋")
        scissors = types.KeyboardButton(text="✌️")
        fireplace = types.KeyboardButton(text="👊")
        keyboard.add(paper, scissors, fireplace, stop)
        await bot.send_message(
            message.chat.id,
            "Добро пожаловать в игру камень ножницы бумага✌️👊🖐️",
            reply_markup=keyboard,
        )
    elif message.text == "/stop":
        keyboard = types.ReplyKeyboardMarkup(
            row_width=3, resize_keyboard=False, one_time_keyboard=False
        )
        start = types.KeyboardButton(text="/start")
        paper = types.KeyboardButton(text="✋")
        scissors = types.KeyboardButton(text="✌️")
        fireplace = types.KeyboardButton(text="👊")
        keyboard.add(paper, scissors, fireplace, start)
        await bot.send_message(
            message.chat.id,
            "игра астановленая",
            reply_markup=keyboard,
        )
    elif message.text == "/help":
        await bot.reply_to(message, "/start - Помогает начать все сначала")


# A response sticker is generated here
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    lst = ["👊", "✋", "✌️"]
    keyboard = types.ReplyKeyboardMarkup(
        row_width=3, resize_keyboard=False, one_time_keyboard=False
    )
    paper = types.KeyboardButton(text="✋")
    scissors = types.KeyboardButton(text="✌️")
    fireplace = types.KeyboardButton(text="👊")
    stop = types.KeyboardButton(text="/stop")
    keyboard.add(paper, scissors, fireplace, stop)
    sleep(0.05)
    await bot.send_message(message.chat.id, lst[randrange(3)], reply_markup=keyboard)


# )
asyncio.run(bot.polling(non_stop=True))
