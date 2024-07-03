<div align="center">
  <h1>AUC Discord Bot</h1>
  <p float="left">
    <img src="/pictures/Yellow.png" width="300" />
    <img src="/pictures/YellowAUC.png" width="300" /> 
  </p>
  <p>
    <i>A discord bot made in the discord.py library for the Antistasi Ultimate Community.</i>
  </p>
  <p>

# FIRST TIME SETUP:
Run `[install].bat`
or
`pip install discord.py requests PyGithub python-a2s`

## Manual Requirements:
Create a file to start the bot. This can be any file that will run the main.py file. In this case we're going to use .bat

Name this file `[start].bat` and inside of it place the code that will run main.py. Example: `py main.py`, `python main.py`

### Token

Create a python file called `bot_token.py` in the root folder and inside it add these 3 variables:
```py
token = BOT_TOKEN # Replace with the bot token, as string
github_login = GITHUB_TOKEN # Replace with the github token, as string
debug = False # Keep as false unless you know exactly what this does
```
github_login can also be account login tuple `("account name", "password")` but this is feature limited.

In order for the command `/restart_bot` to work, [git](https://git-scm.com/download/win) needs to be installed.

# Features:
A ton of slash commands to make life easier. Namely:

Github Integration - Allows admins to create issues, create or merge pull requests, list all open issues/pulls in a repo, etc.

Server integration - The bot can recieve and parse webhook messages formatted by the companion server mod that utilises Pythia.

  </p>  
</div>
