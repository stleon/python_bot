import os
import sys
import asyncio
import subprocess
import telepot
import telepot.async

import commands
from provider import PythonProvider


class PythonBot(telepot.async.Bot):
    def __init__(self, *args, **kwargs):
        super(PythonBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.async.helper.Answerer(self)
        self.provider = PythonProvider()

    @asyncio.coroutine
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print('Chat Message:', content_type, chat_type, chat_id, msg)
        if msg['text'] == '/about':
            yield from self.sendMessage(chat_id, commands.ABOUT)
        elif msg['text'] == '/ping':
            yield from self.sendMessage(chat_id, 'pong')
        elif msg['text'] == '/help':
            yield from self.sendMessage(chat_id, commands.HELP)
        elif msg['text'] == '/python':
            pass
        elif msg['text'] == '/end':
            yield from self.sendMessage(chat_id, 'Nice')
        else:
            print(msg['text'], '!!!!!!!!')
            r = self.provider.execute_command(chat_id, msg['text'])
            yield from self.sendMessage(chat_id, r)


TOKEN = os.getenv('TOKEN')

bot = PythonBot(TOKEN)
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
