import os
from config import TOKEN, TEST_SERVER_ID

from nextcord.ext import commands

# the prefix is not used in this example
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_message(self, message):
    if message.author == self.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')

bot.run('token')
