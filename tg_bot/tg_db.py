from telebot.async_telebot import AsyncTeleBot
import asyncio
import psycopg2

bot = AsyncTeleBot("5692748310:AAHumQcDIHkDgu-7GA_4OlPFtRJYaQ__Bfk")

# Database connection parameters
conn = psycopg2.connect(host="localhost", database="tg", user="serojisahakyan")
cursor = conn.cursor()


# TODO(
# Handle '/allpfilms'
@bot.message_handler(commands=["allfilms"])
async def send_welcome(message):
    if message.text == "/allfilms":
        cursor.execute("SELECT name FROM kino")
        result = cursor.fetchall()
        length_result = len(result)
        if length_result == 0:
            await bot.send_message(message.chat.id, text="Тhe base is empty")
        for tpl in result:
            tpl = str(tpl)
            tpl = tpl[2:-3]
            await bot.send_message(message.chat.id, text=tpl)
            if tpl == result[-1]:
                break


# The reported user is saved here
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    cursor.execute("INSERT INTO kino (name) VALUES ('{}')".format(message.text))
    conn.commit()
    await bot.send_message(message.chat.id, text="Message received!")


asyncio.run(bot.polling(non_stop=True))
