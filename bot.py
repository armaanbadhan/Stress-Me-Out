import interactions
from asyncio import sleep
import sqlite3
import datetime
from config import TOKEN, TEST_SERVER_ID

bot = interactions.Client(token=TOKEN)


conn = sqlite3.connect('deadlines.db')
cursor = conn.cursor()
create_table_script ="""
    CREATE TABLE IF NOT EXISTS deadlines(
        name VARCHAR(255), 
        deadline VARCHAR(255)
    )
"""
cursor.execute(create_table_script)


def change_timeformat(inp: str):
    try:
        due = datetime.datetime.strptime(inp, '%d-%m-%Y-%H:%M')
    except ValueError:
        return "False"
    return due


@bot.command(
    name="stress-me-out",
    description="Shows you the upcoming deadlines",
    scope=TEST_SERVER_ID,
)
async def StressMeOut(ctx: interactions.CommandContext):
    fetch_script = "SELECT * FROM deadlines"
    deadlines = cursor.execute(fetch_script)
    embeded = interactions.Embed(color=0x7289DA)
    added = False
    deadlines = list(deadlines)
    for i in deadlines:
        rec = change_timeformat(i[1])
        embeded.add_field(
            name = i[0],
            value = "OVER" if rec == "False" else "<t:" + str(int(rec.timestamp())) + ":R>",
            inline=False,
        )
        added = True
    if not added:
        embeded.add_field(name="--", value="No upcoming Deadline!")
    await ctx.send(embeds=[embeded])


@bot.command(
    name="add-deadline",
    description="Add a deadline",
    scope=TEST_SERVER_ID,
    options = [
        interactions.Option(
            name="name",
            description="Name of the assignment/quiz",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="date",
            description="date of the deadline",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="month",
            description="month of the deadline",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="time",
            description="time of deadline (in 24hr format) hh:mm",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def add(ctx: interactions.CommandContext, name: str, date: str, month: str, time: str):
    if ctx.author.id != 786851962833862676:
        await ctx.send("youre not authorized")
        return
    time_thing = f"{date}-{month}-2022-{time}"
    insert_script = f"INSERT INTO deadlines VALUES ('{name}', '{time_thing}')"
    cursor.execute(insert_script)
    await ctx.send("Deadline added")


bot.start()