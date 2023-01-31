from config import TOKEN, TEST_SERVER_ID

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

import time
import datetime
from datetime import datetime, timedelta
import dbinteract


bot = commands.Bot(intents=nextcord.Intents.all())


@bot.event
async def on_ready():
    print("bot ready.")


@bot.event
async def on_guild_join(guild):
    await guild.create_role(name='StressedOut')


@bot.slash_command(name="ping", description="example slash command", guild_ids=[TEST_SERVER_ID])
async def ping(interaction: Interaction):
    await interaction.response.send_message("pong")


@bot.slash_command(name="stressmeout", description="Shows The Reminders", guild_ids=[TEST_SERVER_ID])
async def stressmeout(interaction: Interaction):
    embed = nextcord.Embed(title = "Reminders" , description = "Current reminders of this server" , timestamp = datetime.datetime.utcnow())
    
    #add a dummy deadlines
    dbinteract.insert_deadline(TEST_SERVER_ID, "TASK1", 1675904628)
    dbinteract.insert_deadline(TEST_SERVER_ID, "TASK2", 1675904628)
    
    #deadlines is a list of tuples
    deadlines = dbinteract.read_deadline(TEST_SERVER_ID)
    
    
    """
    send the remninder in the form as an discord embed:
    NAME
        DATE
    NAME
        DATE 
    """
        
    for idx in range(len(deadlines)):
        embed.add_field(
                name= str(deadlines[idx][0]),
                value = str(deadlines[idx][1]),
                inline = False
        )
        
    #remove the dummy data
    dbinteract.delete_deadline(TEST_SERVER_ID)
    
    #send the embed
    await interaction.send(embeds=[embed])

@bot.event
async def on_message(message):
    if message.content == '/contests':
        # make API request to kontests.net/api
        response = requests.get("https://kontests.net/api/v1/contests")
        contests = json.loads(response.text)
        
        # filter contests to only show running and upcoming in next 24 hours
        now = datetime.now()
        upcoming_contests = [c for c in contests if (datetime.strptime(c["start"], '%Y-%m-%dT%H:%M:%SZ') - now).days < 1]
        
        # format contest information
        contest_list = "\n".join([f"{c['name']} ({c['start']} - {c['end']})" for c in upcoming_contests])
        
        # send contest information as response to discord
        await message.channel.send(f"Upcoming contests in next 24 hours:\n{contest_list}")

bot.run(TOKEN)
