from config import TOKEN, TEST_SERVER_ID

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

import time
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

    def add_slash_command(name, date, hours, minutes):
    try:
        # Check if the date is in a valid format
        datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

        # Add hours and minutes to the datetime object
        datetime_obj = datetime_obj + datetime.timedelta(hours=int(hours), minutes=int(minutes))

        # Convert the datetime object to unix timestamp
        unix_timestamp = int(datetime_obj.timestamp())

        # Add the data to the database
        # Code to add data to the database

        # Send a confirmation message
        return "Data added successfully with name '{}', date '{} {}:{}' and unix timestamp '{}'".format(name, date, hours, minutes, unix_timestamp)
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD"

    

bot.run(TOKEN)
