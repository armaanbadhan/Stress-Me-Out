import os
import datetime

import nextcord
from nextcord import Interaction, Permissions
from nextcord.ext import commands

import dbinteract
try:
    from config import TOKEN, TEST_SERVER_ID
except ImportError:
    TOKEN = os.environ["TOKEN"]
    TEST_SERVER_ID = os.environ["TEST_SERVER_ID"]


bot = commands.Bot(intents=nextcord.Intents.all())


@bot.event
async def on_ready():
    """
    called once when bot is ready.
    """
    print("bot ready.")


@bot.event
async def on_guild_join(guild):
    """
    Every time a bot joins a server, it create a role named `StressedOut`
    """
    await guild.create_role(name='StressedOut')


@bot.slash_command(
        name="stressmeout",
        description="Shows The Reminders",
        guild_ids=[TEST_SERVER_ID]
    )
async def stressmeout(interaction: Interaction):
    """
    Sends an embed showing all the upcoming deadlines of that server
    """
    embed = nextcord.Embed(
        title="Reminders",
        description="Current reminders of this server",
        timestamp=datetime.datetime.utcnow()
    )
    deadlines = dbinteract.read_deadline(TEST_SERVER_ID)
    length = len(deadlines)
    if length == 0 : 
        embed.description = "Hooray! , No upcoming deadlines"       
    else : 
        for idx in deadlines:
            embed.add_field(name=str(idx[0]), value=str(idx[1]), inline=False)
    await interaction.send(embeds=[embed])


@bot.slash_command(name="add", description="add a reminder", guild_ids=[TEST_SERVER_ID], default_member_permissions=Permissions(administrator=True))
async def add(
        interaction: Interaction,
        reminder_name: str,
        date: str,
        month: str,
        year: str,
        hour: str,
        minutes: str
    ):
    """
    To add a deadline in a server
    """
    # TODO: only people with `StressedOut` role and admins should be able to call this command

    deadline = date + month + year + " " + hour + ":" + minutes

    try:
        deadline_time = datetime.datetime.strptime(deadline, "%d%m%Y %H:%M")

        if datetime.datetime.now() > deadline_time:
            await interaction.response.send_message("Date has already expired!")
            return

        flag = dbinteract.insert_deadline(
                TEST_SERVER_ID,
                reminder_name,
                deadline_time.isoformat()
            )

        if flag:
            await interaction.response.send_message("Successfully added a reminder!")
        else:
            await interaction.response.send_message("The name " + reminder_name + \
                                                    " already exists in the table! ")

    except ValueError:
        await interaction.response.send_message("The Time format is invalid! Please try again.")


bot.run(TOKEN)
