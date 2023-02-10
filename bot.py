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
    embed = nextcord.Embed(title = "Reminders", description = "Current reminders of this server", timestamp = datetime.datetime.utcnow())
    deadlines = dbinteract.read_deadline(TEST_SERVER_ID)
    for idx in range(len(deadlines)):
        embed.add_field(name= str(deadlines[idx][0]), value = str(deadlines[idx][1]), inline = False)
    await interaction.send(embeds=[embed])


@bot.slash_command(name="add", description="add a reminder", guild_ids=[TEST_SERVER_ID])
async def add(interaction: Interaction, reminder_name: str, date: str, month: str, year: str, hour: str, minutes: str):

    #noting the current time
    curr_time = datetime.datetime.now()
    curr_time = datetime.datetime.strftime(curr_time, '%d%m%Y %H:%M')

    #deadline format: 20082002 12:05
    date = date + month + year
    deadline = date + " " + hour + ":" + minutes 
    
    try:
        deadline_time = datetime.datetime.strptime(deadline, "%d%m%Y %H:%M")

        if curr_time > deadline_time: 
            await interaction.response.send_message("Date has already expired!")
        else:
            flag = dbinteract.insert_deadline(TEST_SERVER_ID, reminder_name, deadline_time.isoformat())
            
            if flag: await interaction.response.send_message("Successfully added a reminder!")
            else: await interaction.response.send_message("The name " + reminder_name + " already exists in the table! ")

    except ValueError as ve:
        await interaction.response.send_message("The Time format is invalid! Please try again.")

    
    
    

bot.run(TOKEN)
