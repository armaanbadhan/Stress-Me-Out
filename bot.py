import discord


with open("token.txt", 'r') as fi:
    TOKEN = fi.read()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == '$show':
            await message.channel.send('Deadlines: \nplaceholder 1\nplaceholder 2')
        
        if message.content == '$add':
            await message.channel.send('deadline added')

        if message.content == '$remove':
            await message.channel.send('removed deadline')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
