import openai
import telebot
from os import getenv
from random import random



openai.api_key = getenv('API_KEY')
token = getenv('TOKEN')

bot = telebot.TeleBot(token)
content_types = ['audio', 'document', 'photo', 'sticker', 'video', 'video_note',\
                'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member',\
                'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',\
                'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',\
                'migrate_from_chat_id', 'pinned_message']

@bot.message_handler(content_types=content_types)
def acceptable_content(message):
    if message.chat.type != 'group' and message.chat.type != 'supergroup':
        bot.send_message(message.chat.id, 'На данный момент я понимаю только текст😑')


@bot.message_handler()
def message_handler(message):
    if message.text in ['/start', '/help']:
        mess = f'Привет, <b>{message.from_user.first_name}</b>, я твой верный помошник, '\
        'ты можешь задать мне любой вопрос и я отвечу😊'
        bot.send_message(message.chat.id, mess, parse_mode = 'html')
    else:
        message_log = [{"role": "system", "content": "Ты сарказм бот, говоришь на русском"}]
        conversation(message, message_log)


def conversation(message, message_log):
    query = message.text
    if not query:
        if message.chat.type != 'group' and message.chat.type != 'supergroup':
            bot.send_message(message.chat.id, 'На данный момент я понимаю только текст')
        bot.register_next_step_handler(message, conversation, message_log)
        return
    elif query in ['/clear', '/clear@great_ai_oracle_bot']:
        bot.clear_step_handler_by_chat_id(chat_id = message.chat.id)
        bot.send_message(message.chat.id, 'Чат очищен, можете начать другой диалог')
        return
    if (message.chat.type == 'group' or message.chat.type == 'supergroup') and bot.get_me().username not in query and not message.reply_to_message:
            if random() < 0.9:
                bot.register_next_step_handler(message, conversation, message_log)
                return
    elif (message.chat.type == 'group' or message.chat.type == 'supergroup') and bot.get_me().username not in query and message.reply_to_message:
        if message.reply_to_message.from_user.id != bot.get_me().id:
            if random() < 0.9:
                bot.register_next_step_handler(message, conversation, message_log)
                return
    message_log.append({'role': 'user', 'content': query})
    bot.send_chat_action(message.chat.id, 'typing')
    response = send_message(message_log)
    message_log.append({'role': 'assistant', 'content': response})
    bot.send_message(message.chat.id, response, parse_mode = 'html')
    bot.register_next_step_handler(message, conversation, message_log)


def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=1000,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=1.1,        # The "creativity" of the generated response (higher temperature = more creative)
    )
    return response['choices'][0]['message']['content']


bot.infinity_polling()