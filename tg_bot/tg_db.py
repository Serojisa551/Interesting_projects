from telebot.async_telebot import AsyncTeleBot, types
import asyncio
import psycopg2

bot = AsyncTeleBot("5692748310:AAHumQcDIHkDgu-7GA_4OlPFtRJYaQ__Bfk")

# Database connection parameters
conn = psycopg2.connect(host="localhost", database="tg", user="serojisahakyan")
cursor = conn.cursor()


# TODO(
# Handle '/allpfilms', '/start' and '/deleteall'
@bot.message_handler(commands=["allfilms", "start", "deleteall"])
async def send_welcome(message):
    if message.text == "/deleteall":
        markup = types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton("yes", callback_data="del_yes")
        no = types.InlineKeyboardButton("no", callback_data="del_no")
        markup.add(yes, no)
        await bot.send_message(
            message.chat.id,
            text="Are you sure you want to delete everything",
            reply_markup=markup,
        )
    if message.text == "/start":
        await bot.send_message(
            message.chat.id, text="The bot is activated and ready to work"
        )
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


# Here the button click is being processed
@bot.callback_query_handler(func=lambda call: True)
async def callback(call):
    if call.message:
        if call.data == "del_yes":
            cursor.execute("TRUNCATE TABLE kino")
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text="Аll deleted successfully",
            )
        if call.data == "del_no":
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text="Okay I left the process",
            )


# The reported user is saved here
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    cursor.execute("INSERT INTO kino (name) VALUES ('{}')".format(message.text))
    conn.commit()
    await bot.send_message(message.chat.id, text="Message received!")


asyncio.run(bot.polling(non_stop=True))
