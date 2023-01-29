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
    
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name = 'StressedOut')
    await.client.add_roles(member, role)
                             


@bot.slash_command(name="ping", description="asdf", guild_ids=[TEST_SERVER_ID])
async def ping(interaction: Interaction):
    await interaction.response.send_message("pong")


@bot.slash_command(name="stressmeout", description="Shows The Reminders", guild_ids=[TEST_SERVER_ID])
async def stressmeout(interaction: Interaction):
    embed = nextcord.Embed(title = "Reminders" , description = "Current reminders of this server" , timestamp = datetime.datetime.utcnow())
    
    embed.set_author(name = "Request by " + interaction.user.name)
    embed.set_footer(text="Made by Armaan" , icon_url= "https://th.bing.com/th/id/OIP.-dFvAYTcGIX85iRztBlAzAAAAA?pid=ImgDet&w=474&h=474&rs=1")

    
    #create deadlines table and add a dummy deadline
    dbinteract.create_deadlines_table()
    dbinteract.insert_deadline(TEST_SERVER_ID,"TASK", 24082023)
    
    #deadlines is a list of tuples
    deadlines = dbinteract.read_deadline(TEST_SERVER_ID)
    
    
    """send the remninder in the form as an discord embed:
    NAME ---> DATE
    NAME ---> DATE """
        
    for idx in range(len(deadlines)):
        embed.add_field(
                name= str(deadlines[idx][0])+ "  " + str(deadlines[idx][1]),
                value = "",
                inline = False 
                )
        
    #remove the dummy table
    dbinteract.delete_all_data()
    
    #send the embed
    await interaction.send(embed = embed)


    

bot.run(TOKEN)
