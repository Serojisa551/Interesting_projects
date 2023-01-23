from telebot.async_telebot import AsyncTeleBot, types
from random import randrange
import asyncio

bot = AsyncTeleBot("5710299504:AAFoermLvSR-MUNcLADs2FuyWCDxkAiJh4o")

#TODO(
# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
async def send_welcome(message):
    if message.text == "/start":
        keyboard = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=False, one_time_keyboard=False
        )
        tuxt1 = types.KeyboardButton(text="✋")
        mkrat1 = types.KeyboardButton(text="✌️")
        qar1 = types.KeyboardButton(text="👊")
        keyboard.add(tuxt1, mkrat1, qar1)
        await bot.send_message(
            message.chat.id, "Добро пожаловать в игру камень ножницы бумага✌️👊🖐️", reply_markup=keyboard
        )
        pass
    elif message.text == "/help":
        await bot.reply_to(message, "/start - helps to start again.")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    lst = ["👊", "✋", "✌️"]
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=False, one_time_keyboard=False
    )
    tuxt1 = types.KeyboardButton(text="✋")
    mkrat1 = types.KeyboardButton(text="✌️")
    qar1 = types.KeyboardButton(text="👊")
    keyboard.add(tuxt1, mkrat1, qar1)
    await bot.send_message(
        message.chat.id, "💥💥💥", reply_markup=keyboard
    )
    await bot.send_message(message.chat.id, lst[randrange(3)])


asyncio.run(bot.polling(non_stop = True))#)
