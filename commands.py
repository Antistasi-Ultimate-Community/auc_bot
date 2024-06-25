import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from config import guild_id
from config import guild_roles_moderator
from config import guild_error_notmoderator
from config import guild_log_file
from config import guild_log_init
from config import url_missing

from access import is_admin
from access import is_moderator
from access import is_channel_bot

from mg_init import init

from log import log_message

from typing import Literal

from web import format_embed
from web import send_changelog
from web import send_message
from web import check_url
from web import return_url
from web import send_url

import time

class changelog_modal(ui.Modal):
    def __init__(self, mod_type):
        self.mod_type = mod_type
        super().__init__(title='Changelog Form')

    version_textinput = ui.TextInput(label="Version", default="10.0.0")
    changelog_url_textinput = ui.TextInput(label="Changelog URL", default="https://antistasiultimate.com")
    changelog_textinput = ui.TextInput(label="Changelog", style=discord.TextStyle.paragraph, default="This is a changelog!", max_length=930)

    async def on_submit(self, interaction: discord.Interaction):
        embed = send_changelog(interaction=interaction, changelog={"version": self.version_textinput, "changelog": [self.changelog_textinput, self.changelog_url_textinput]}, mod_type=self.mod_type)
        await embed

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

    return message_send

def commands_init(client):

    tree = app_commands.CommandTree(client)

    @tree.command(name="utility_message", description="Sends a utility message.", guild=guild_id)
    @app_commands.check(is_moderator)
    async def utility_message(interaction: discord.Interaction, message: Literal["PAA Converter", "Discord Link", "Server Info", "Map Names"]):
        message_send = handle_utility_message(message)
        message_response = send_message(interaction=interaction, message=message_send, local=False)
        await message_response

    @tree.command(name="embed", description="Embeds a message with given args.", guild=guild_id)
    @app_commands.check(is_admin)
    async def embed(interaction: discord.Interaction, title: str = None, description: str = None, colour: int = 15844367, thumbnail: str = "https://antistasiultimate.com/images/UACLogoSmall.png"):
        embed = format_embed(interaction=interaction, title=title, description=description, colour=colour, thumbnail=thumbnail)
        await interaction.response.send_message(embed=embed)
            
    @tree.command(name="changelog", description="Creates a changelog form using an embed.", guild=guild_id)
    @app_commands.check(is_admin)
    async def changelog(interaction: discord.Interaction, mod_type: Literal["Main", "Public Testing"]):
        await interaction.response.send_modal(changelog_modal(mod_type))

    @tree.command(name="shutdown", description="Shuts down the bot.", guild=guild_id)
    @app_commands.check(is_admin)
    async def shutdown(interaction: discord.Interaction, confirm: bool):
        if (confirm):
            message = send_message(interaction=interaction, message=f"Shutting down the bot now.", local=False)
            await message

            log_message(-1, (f"{interaction.user.display_name} ({interaction.user.id}) is attempting shutdown."), header=guild_log_init, space=True)
            log_message(-1, (f"We have logged out of {client.user}. ID: {client.user.id}"), header=guild_log_init, space=True)
            await client.close() # probably best to await the client to close itself, as it spams errors before shutting down otherwise

            exit()
            # should move this to its own function (outside of commands) so it can be used in other places
        else:
            message = send_message(interaction=interaction, message=f"Shutdown was not confirmed.", local=True)
            await message

    @tree.command(name="custom_message", description="Send a custom message.", guild=guild_id)
    @app_commands.check(is_admin)
    async def custom_message(interaction: discord.Interaction, text: str):
        message = send_message(interaction=interaction, message=text, local=False)
        await message

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

    @tree.command(name="generate_modset_help", description="Shows all of the parameters for generate_modset.", guild=guild_id)
    async def generate_modset_help(interaction: discord.Interaction):
        help_message = "# USE A COMMA (,) BETWEEN EACH PARAMETER, AND DON'T USE SPACES.\nhttps://github.com/Antistasi-Ultimate-Community/auc_bot/wiki/Modset-Generator"
        message = send_message(interaction=interaction, message=help_message, local=True)
        await message

    @tree.command(name="generate_modset", description="Generates a modset with given parameters.", guild=guild_id)
    async def generate_modset(interaction: discord.Interaction, modsets: str, climates: str = "", era: Literal["modern", "scifi", "lowtech", "coldwar", "stalker"] = "", key: Literal["vanilla", "rhs"] = "", dlc: str = "", double_occ: bool = False, simple: bool = True):
        modsets = modsets.split(",")
        climates = climates.split(",")
        dlc = dlc.split(",")
        log_msg = f"{interaction.user.display_name} ({interaction.user.id}) is generating a modset."
        log_message(-1, log_msg)

        modset_message = init(modsets=modsets, climates=climates, era=era, key=key, dlc=dlc, double_occ=double_occ, simple=simple)
        embed = format_embed(interaction=interaction, title="Modset Generator", description=modset_message)
        message = interaction.response.send_message(embed=embed)
        # message = send_message(interaction=interaction, message=modset_message, local=False)
        await message

    @utility_message.error
    @changelog.error
    @embed.error
    @shutdown.error
    @custom_message.error
    @pull.error
    @issue.error
    @wiki.error
    @generate_modset_help.error
    @generate_modset.error
    async def say_error(interaction : discord.Interaction, error):
        await send_message(interaction, error, local=True)

    return tree