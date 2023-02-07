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


@bot.event
async def on_guild_join(guild):
    await guild.create_role(name='StressedOut')


@bot.slash_command(name="ping", description="example slash command", guild_ids=[TEST_SERVER_ID])
async def ping(interaction: Interaction):
    await interaction.response.send_message("pong")


@bot.slash_command(name="stressmeout", description="Shows The Reminders", guild_ids=[TEST_SERVER_ID])
async def stressmeout(interaction: Interaction):
    embed = nextcord.Embed(title = "Reminders" , description = "Current reminders of this server" , timestamp = datetime.datetime.utcnow())
    
    #remove the dummy data
    dbinteract.delete_deadline(TEST_SERVER_ID)
        
    #add a dummy deadlines
    dbinteract.insert_deadline(TEST_SERVER_ID, "TASK1", "2023-02-08T11:34:20.753583")
    dbinteract.insert_deadline(TEST_SERVER_ID, "TASK1", "2023-02-09T11:34:20.753583")
    
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


    

bot.run(TOKEN)
