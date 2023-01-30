import os
from config import TOKEN, TEST_SERVER_ID

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

import datetime
import dbinteract


bot = commands.Bot(intents=nextcord.Intents.all())


@bot.event
async def on_ready():
    print("bot ready.")


@bot.slash_command(name="ping", description="asdf", guild_ids=[TEST_SERVER_ID])
async def ping(interaction: Interaction):
    await interaction.response.send_message("pong")


@bot.slash_command(name="stressmeout", description="Shows The Reminders", guild_ids=[TEST_SERVER_ID])
async def stressmeout(interaction: Interaction):
    embed = nextcord.Embed(title = "Reminders" , description = "Current reminders of this server" , timestamp = datetime.datetime.utcnow())
    
    #add a dummy deadlines
    dbinteract.insert_deadline(TEST_SERVER_ID, "TASK1", 24082023)
    dbinteract.insert_deadline(TEST_SERVER_ID, "TASK2", 24082023)
    
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
    dbinteract.delete_all_data()
    
    #send the embed
    await interaction.send(embeds=[embed])


    

bot.run(TOKEN)
