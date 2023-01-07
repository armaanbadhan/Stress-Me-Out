import os
from config import TOKEN, TEST_SERVER_ID

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

# the prefix is not used in this example
bot = commands.Bot(intents=nextcord.Intents.all())


@bot.event
async def on_ready():
    print("bot ready.")


@bot.slash_command(name="ping", description="asdf", guild_ids=[TEST_SERVER_ID])
async def ping(interaction: Interaction):
    await interaction.response.send_message("pong")


# initial_extensions = []

# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         initial_extensions.append('cogs.' + filename[:-3])



# for extension in initial_extensions:
#     bot.load_extension(extension)

bot.run(TOKEN)
