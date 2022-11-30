import interactions

with open("token.txt", 'r') as fi:
    TOKEN = fi.read().strip()

bot = interactions.Client(token=TOKEN)

@bot.command(
    name="stress-me-out",
    description="Shows you the upcoming deadlines",
    scope=1039826459503644704,
)
async def StressMeOut(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

bot.start()
