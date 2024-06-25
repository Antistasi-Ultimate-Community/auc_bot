import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from config import guild_id
from config import git_client

from access import is_admin

from typing import Literal

from handle_git import grab_issues

from log import log_message

from web import send_message
from web import send_changelog
from web import format_embed

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

def commands_admin(client, tree):
    
    @tree.command(name="list_open_docs", description="Lists open issues/pull requests on the Antistasi Ultimate wiki.", guild=guild_id)
    @app_commands.check(is_admin)
    async def list_open_docs(interaction: discord.Interaction, type: Literal["issue", "pull"] = ""):

        await interaction.response.defer(thinking=True)
        
        issues = grab_issues(git_client=git_client, type=type)

        text = issues[1]

        embed = format_embed(interaction=interaction, title=f"{type}s", description=text)

        # message = send_message(interaction=interaction, message=text, local=False, just_message=True)
        await interaction.followup.send(embed=embed)

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
        else:
            message = send_message(interaction=interaction, message=f"Shutdown was not confirmed.", local=True)
            await message

    @tree.command(name="custom_message", description="Send a custom message.", guild=guild_id)
    @app_commands.check(is_admin)
    async def custom_message(interaction: discord.Interaction, text: str):
        message = send_message(interaction=interaction, message=text, local=False)
        await message

    @list_open_docs.error
    @changelog.error
    @embed.error
    @shutdown.error
    @custom_message.error
    async def say_error(interaction : discord.Interaction, error):
        await send_message(interaction, error, local=True)