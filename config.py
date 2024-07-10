import discord
from discord import app_commands

from bot_token import debug
from bot_token import github_login

from datetime import date
from datetime import datetime

from main_git import start_git_client

import os

# Need to convert most of the variables in this file to json, that way we can add/remove during runtime

def guild_day_time(type="", type_format=""):
    if (type == ""):
        exit()

    if (type == "day"):
        day = date.today()
        return day
    
    if (type == "time" and (type_format != "")):
        time = datetime.now().strftime(type_format)
        return time

    return False

day = guild_day_time("day")
time = guild_day_time("time", "%H-%M-%S")

print(f"{day}_{time}")

if (debug):
    #DEBUG
    guild_id = discord.Object(599612913879351300)
    guild_roles_admin = []
    guild_roles_moderator = guild_roles_admin + []
    guild_roles_log_exempt = guild_roles_moderator + []
    guild_channel_log_exempt = [599612914567086091]
    guild_channel_bot = 1255143195097043005
    guild_name_bot = "AUC"
else:
    #NORMAL
    guild_id = discord.Object(817005365740044289)
    guild_roles_admin = [817012725183807509] # Admin
    guild_roles_moderator = guild_roles_admin + [1246558470082134098, 817012746608443412, 1143194227187122208, 1016040774581882950] # Head Moderator, Moderator, Staff, Dev
    guild_roles_log_exempt = guild_roles_moderator + [1151867794418311209, 1218816913107451984, 1241819466371960836] # Dev Helper, Texture Dev, AUC
    guild_channel_log_exempt = [817005366189621279]
    guild_channel_bot = 1255143679929090098
    guild_name_bot = "AUC"

guild_log_file = f"logs/{day}_{time}-discord.log"
guild_log_init = f"Bot initialization"
guild_log_copyright = f"Copyright © 2023 - 2024 Antistasi Ultimate All Rights Reserved"

git_repo_base = "https://github.com"

guild_git_repo_normal = f"SilenceIsFatto/A3-Antistasi-Ultimate"
guild_git_repo_debug = f"Antistasi-Ultimate-Community/testing-grounds"
guild_git_repo_bot = f"{git_repo_base}/Antistasi-Ultimate-Community/auc_bot"

if (debug):
    guild_git_repo = guild_git_repo_debug
    guild_user_webhook_id = 1257005684185366579
else:
    guild_git_repo = guild_git_repo_normal
    guild_user_webhook_id = 1256738636364517426

pull_request_template = """
## What type of PR is this?
1. [ ] Bug
2. [ ] Change
3. [ ] Enhancement
4. [ ] Miscellaneous

### What have you changed and why?
Information:

### Please specify which Issue this PR Resolves (If Applicable).
"This PR closes #XXXX!"

### Please verify the following.

1. [ ] Have you loaded the mission in LAN host?
2. [ ] Have you loaded the mission on a dedicated server?

### Is further testing or are further changes required?

1. [ ] No
2. [ ] Yes (Please provide further detail below.)

### How can the changes be tested?
Steps:

********************************************************
Notes:
"""

guild_error_notmoderator = "You are not allowed to use this command."

def guild_log_spacer(message):
    spacer = f"\--------- {message} ---------/"

    return spacer

guild_log_modset_init_start = guild_log_spacer("Starting modset init.")
guild_log_modset_init_finish = guild_log_spacer("Finished modset init.")

def url_missing(interaction, local=True):
    return interaction.response.send_message("This URL doesn't exist or is returning 404.", ephemeral=local)

def grab_exempt_channels(client):
    # Convert ID to actual channel
    exempt_channels = []
    for channel_id in guild_channel_log_exempt:
        channel = client.get_channel(channel_id)
        exempt_channels.append(channel)

    return exempt_channels

async def shutdown(client):
    print(f"We have logged out of {client.user}. ID: {client.user.id}")

    await send_log(client)
    
    await client.close() # probably best to await the client to close itself, as it spams errors before shutting down otherwise

    exit()

async def send_log(client, interaction=None):
    channel_bot = client.get_channel(guild_channel_bot)

    if (interaction == None):
        await channel_bot.send(file=discord.File(guild_log_file))
    else:
        await interaction.response.send_message(file=discord.File(guild_log_file), ephemeral=True)


git_client = start_git_client(github_login=github_login)