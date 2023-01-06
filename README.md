# Stress-Me-Out

A discord bot which helps in maintaining assignment deadlines and upcoming quizzes. Users can also subscribe to our reminder system to get a notification 2 hours before the submission. A daily reminder is also sent at 10 am. Admins of the server can assign supserusers who can add/modify/delete reminders. Users can see reminders on slash command and can subscribe to reminders.



### To run the bot

1. Go to https://discord.com/developers/applications and log in.

2. Click on `New Application` enter the name, and create.

3. Go to `Bot` -> `Add Bot`, Enable `PRESENCE INTENT`, `SERVER MEMBERS INTENT` and `MESSAGE CONTENT INTENT`.

4. Click on reset token to generate a new token, and then click copy. Paste this in your project's config file. We have successully created a bot, now we add it to our server.

5. To add the bot to our server we will generate a link. Go to `OAuth2` -> `URL Generator`. In Scope add `BOT` and `applications.commands`. and in `BOT PREMISSIONS` give the perms: `Manage Roles, Read Messages/View Channels, Send Messages`. Then copy the generated url and paste it in a new tab. Add to any server you want (preferably create a new server just to test out the bot). You can always come back to this page and grant new permissions to your bot and add it again.

Now a bot is created and added to the server.

[You can also refer to these docs](https://docs.nextcord.dev/en/stable/discord.html)


## Contribute

##### 1. Fork the Repository
To contribute, fork this repository to your own github account.

##### 2. Clone the project
```bash
    git clone https://github.com/armaanbadhan/Stress-Me-Out.git
```

##### 3. Go to the project directory
```bash
    cd Stress-Me-Out
```

##### 4. Install dependencies
```bash
    pip install -r requirements.txt
```

##### 5. Create the config.py file 
Create a config.py file from config.py.example, Add your token and the server id of the server you added your bot to. To get the server ID right click on the server -> Copy ID. if the copy id option is not visible, turn on developer options in discord settings. MAKE SURE TOKEN IS NEVER SHARED.

##### 6. Run script
```bash
    python bot.py
```

### This Project uses [nextcord](https://github.com/nextcord/nextcord), docs can be found [here](https://docs.nextcord.dev/en/stable/)