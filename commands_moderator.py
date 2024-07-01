import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from config import guild_id

from access import is_moderator

from typing import Literal

from log import log_message

from web import send_message
from web import send_url
from web import send_changelog
from web import check_url
from web import format_embed

from steam_server import grab_server
from datetime import timedelta

def handle_utility_message(message):
    log_message(-1, message)
    
    # This may be a crime but sometimes criminals do the wrong things for the right reasons
    if (message == "PAA Converter"):
        message_send = f"PAA Converter Website:\nhttps://paa.gruppe-adler.de/"

    if (message == "Discord Link"):
        message_send = "https://discord.gg/antistasiultimate"
        
    if (message == "Server Info"):
        message_send = f"To get started, head over to https://discord.com/channels/817005365740044289/817012040673001492 and choose a server modlist.\nOnce you've downloaded the mods, you'll need to go to https://discord.com/channels/817005365740044289/817005366189621280.\nFind the server number that matches the one you picked in the first step. Use that info with the arma launcher direct connect button.\n\nYou can use https://discord.com/channels/817005365740044289/847499650637758484 to see if people are on the server(s).\nIf you encounter issues or want to discuss something server related, use https://discord.com/channels/817005365740044289/1218157984824295505!"

    if (message == "Map Names"):
        message_send = "https://discord.com/channels/817005365740044289/1208764622455185418"

    if (message == "Saves"):
        message_send = "Save location: `Documents\\Arma 3 (+ Other Profiles\\Name)`\nName.Arma3Profile\nName.vars.Arma3Profile\nAntistasiPlus.vars\nIf transferring to server: Rename 'Name' to match the servers name."

    return message_send

def commands_moderator(client, tree):
    
    @tree.command(name="utility_message", description="Sends a utility message.", guild=guild_id)
    @app_commands.check(is_moderator)
    async def utility_message(interaction: discord.Interaction, message: Literal["PAA Converter", "Discord Link", "Server Info", "Map Names", "Saves"]):
        message_send = handle_utility_message(message)
        message_response = send_message(interaction=interaction, message=message_send, local=False)
        await message_response

    @tree.command(name="pull", description="Link a PR from the Antistasi Ultimate github.", guild=guild_id)
    @app_commands.check(is_moderator)
    async def pull(interaction: discord.Interaction, pr_index: int):
        if (not isinstance(pr_index, int)):
            return False

        url = f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/pull/{pr_index}"
        message = send_url(interaction=interaction, url=url, local=False, suppress=True)
        await message

    @tree.command(name="issue", description="Link an issue from the Antistasi Ultimate github.", guild=guild_id)
    @app_commands.check(is_moderator)
    async def issue(interaction: discord.Interaction, issue_index: int):
        if (not isinstance(issue_index, int)):
            return False
            
        url = f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/issues/{issue_index}"
        message = send_url(interaction=interaction, url=url, local=False, suppress=True)
        await message

    @tree.command(name="wiki", description="Link the Antistasi Ultimate wiki.", guild=guild_id)
    @app_commands.check(is_moderator)
    async def wiki(interaction: discord.Interaction, wiki_page: Literal["FAQ", "Arms-Dealer", "Features", "Maps", "Mods", "Extender-Addons", "Developers", "Developer-Documentation"] = "", reply_target: str = ""):

        if (wiki_page != ""):
            url = f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/wiki/{wiki_page}"
        else:
            url = f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/wiki"

        if (check_url(url=url) != True):
            return False

        if (reply_target != "" and ("@" in reply_target)):
            url = f"{reply_target}\n{url}"

        message = send_message(interaction=interaction, message=url, local=False)
        await message

    @tree.command(name="players", description="Lists all players currently on a server (Default: Server 3).", guild=guild_id)
    @app_commands.check(is_moderator)
    async def players(interaction: discord.Interaction, duration: bool = False, ip: str = None, port: int = None):

        server = grab_server(ip=ip, port=port)

        server_players = server[1]

        players = "```"

        for server_player in server_players:
            if (duration):
                duration = "{:0>8}".format(str(timedelta(seconds=round(server_player.duration))))
                players = f"{players}\n{server_player.name} - {duration}"
            else:
                players = f"{players}\n{server_player.name}"

        players = f"{players}```"

        message = send_message(interaction=interaction, message=players, local=False)
        await message

    @utility_message.error
    @pull.error
    @issue.error
    @wiki.error
    @players.error
    async def say_error(interaction : discord.Interaction, error):
        await send_message(interaction, error, local=True)