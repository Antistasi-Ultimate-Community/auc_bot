import discord
from discord import app_commands

from bot_token import debug

from datetime import date
from datetime import datetime

from main_git import start_git_client

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
    guild_roles_admin = [599615857378983973]
    guild_roles_moderator = guild_roles_admin + []
    guild_roles_log_exempt = guild_roles_moderator + []
    guild_channel_bot = 1255143195097043005
    guild_name_bot = "AUC"
else:
    #NORMAL
    guild_id = discord.Object(817005365740044289)
    guild_roles_admin = [817012725183807509] # Admin
    guild_roles_moderator = guild_roles_admin + [1246558470082134098, 817012746608443412, 1143194227187122208, 1016040774581882950] # Head Moderator, Moderator, Staff, Dev
    guild_roles_log_exempt = guild_roles_moderator + [1151867794418311209, 1218816913107451984, 1241819466371960836] # Dev Helper, Texture Dev, AUC
    guild_channel_bot = 1255143679929090098
    guild_name_bot = "AUC"

guild_log_file = f"logs/{day}_{time}-discord.log"
guild_log_init = f"Bot initialization"
guild_log_copyright = f"Copyright © 2023 - 2024 Antistasi Ultimate All Rights Reserved"

def guild_log_spacer(message):
    spacer = f"\--------- {message} ---------/"

    return spacer

guild_log_modset_init_start = guild_log_spacer("Starting modset init.")
guild_log_modset_init_finish = guild_log_spacer("Finished modset init.")

guild_error_notmoderator = "You are not allowed to use this command."

def url_missing(interaction, local=True):
    return interaction.response.send_message("This URL doesn't exist or is returning 404.", ephemeral=local)

git_client = start_git_client()