# auc_bot
A discord bot made in discord.py for the Antistasi Ultimate Community.

# FIRST TIME SETUP:
Run `[install].bat`
or
`pip install discord.py requests`

## Manual Requirements:
Create a file to start the bot. This can be any file that will run the main.py file. In this case we're going to use .bat

Name this file `[start].bat` and inside of it place the code that will run main.py. Example: `py main.py`, `python main.py`

### Token

Create a python file called `bot_token.py` in the root folder and inside it add these 2 variables:
```py
token = BOT_TOKEN # Replace with the bot token, as string
debug = False # Debug will run this on the specified "guild" (discord server) that is set in config.py
# This means that slash commands and such will only sync with that "guild". Right now it's set to my testing server
```

# Features:
A ton of slash commands to make life easier.
