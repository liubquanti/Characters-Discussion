import telebot
import asyncio
import random
import config
from characterai import aiocai

bot1 = telebot.TeleBot(config.BOT1TOKEN)
bot2 = telebot.TeleBot(config.BOT2TOKEN)

characterai_client1 = aiocai.Client(config.CHARTOKEN)
characterai_client2 = aiocai.Client(config.CHARTOKEN)
previous_chat_id1 = None
previous_chat_id2 = None

async def get_character_ai_response(client, character_id, message_text, previous_chat_id):
    async with await client.connect() as chat:
        me = await client.get_me()
        if previous_chat_id:
            response = await chat.send_message(character_id, previous_chat_id, message_text)
        else:
            new_chat, answer = await chat.new_chat(character_id, me.id)
            previous_chat_id = new_chat.chat_id
            response = await chat.send_message(character_id, previous_chat_id, message_text)
        return response.text, previous_chat_id


async def character_discussion():
    global previous_chat_id1, previous_chat_id2
    message1 = "Hi im Akane Kurokawa, nice to meet ya!"
    message2 = "I am Kana Arima B-Komachi's Idol, Nice to meet you!"

    while True:
        response1, previous_chat_id1 = await get_character_ai_response(
            characterai_client1, config.CHARACTER1ID, message2, previous_chat_id1
        )
        bot1.send_message(config.CHANNEL, f"{response1}")
        await asyncio.sleep(random.randint(2, 5))

        response2, previous_chat_id2 = await get_character_ai_response(
            characterai_client2, config.CHARACTER2ID, response1, previous_chat_id2
        )
        bot2.send_message(config.CHANNEL, f"{response2}")
        await asyncio.sleep(random.randint(2, 5))

if __name__ == '__main__':
    asyncio.run(character_discussion())
