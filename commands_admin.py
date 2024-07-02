import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from config import guild_id
from config import git_client
from config import guild_log_init
from config import shutdown
from config import guild_git_repo
from config import guild_git_repo_debug
from config import send_log

from access import is_admin

from typing import Literal

from handle_git import grab_repo
from handle_git import grab_pulls_merge_ready
from handle_git import grab_issues
from handle_git import open_issue
from handle_git import open_pull
from handle_git import merge_pull
from handle_git import merge_pulls
from handle_git import update_branch

from handle_git_cmd import update_bot

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
    
    # need to implement an optional "repository" argument for each "git_" command
    @tree.command(name="git_list", description="Lists open issues/pull requests.", guild=guild_id)
    @app_commands.check(is_admin)
    async def git_list(interaction: discord.Interaction, type: Literal["issues", "pull"], local: bool = True):

        await interaction.response.defer(thinking=True, ephemeral=local)

        repo = grab_repo(git_client=git_client, repository=guild_git_repo)
        
        issues = grab_issues(git_client=git_client, type=type, repo=repo)

        text = issues[1]

        embed = format_embed(interaction=interaction, title=f"{type}", description=text)

        # message = send_message(interaction=interaction, message=text, local=False, just_message=True)
        await interaction.followup.send(embed=embed, ephemeral=local)

    @tree.command(name="git_branch_update", description="Updates a branch with unstable.", guild=guild_id)
    @app_commands.check(is_admin)
    async def git_branch_update(interaction: discord.Interaction, base: str, head: str):
        repo = grab_repo(git_client=git_client, repository=guild_git_repo)
        branch = update_branch(repo=repo, base=base, head=head)

        message = send_message(interaction=interaction, message=branch, local=False)
        await message

    @tree.command(name="git_pull_merge_ready", description="Merges all pull requests with the 'ready-for-merge' tag.", guild=guild_id)
    @app_commands.check(is_admin)
    async def git_pull_merge_ready(interaction: discord.Interaction):

        await interaction.response.defer(thinking=True)

        repo = grab_repo(git_client=git_client, repository=guild_git_repo)
        pulls = grab_pulls_merge_ready(git_client=git_client, repo=repo)

        pulls_numbers = pulls[1]

        pulls_merged = merge_pulls(repo=repo, numbers=pulls_numbers)

        message = send_message(interaction=interaction, message=pulls_merged, local=False, just_message=True)

        await interaction.followup.send(message)

    @tree.command(name="git_pull_merge", description="Merges a pull request.", guild=guild_id)
    @app_commands.check(is_admin)
    async def git_pull_merge(interaction: discord.Interaction, number: int):
        repo = grab_repo(git_client=git_client, repository=guild_git_repo)
        pull = merge_pull(repo=repo, number=number)

        message = send_message(interaction=interaction, message=pull, local=False)
        await message

    @tree.command(name="git_pull_create", description="Creates a pull request.", guild=guild_id)
    @app_commands.check(is_admin)
    async def git_pull_create(interaction: discord.Interaction, base: str, head: str, title: str = "", body: str = ""):
        repo = grab_repo(git_client=git_client, repository=guild_git_repo)
        pull = open_pull(repo=repo, base=base, head=head, title=title, body=body, author=interaction.user.display_name)

        message = send_message(interaction=interaction, message=pull, local=False)
        await message

    @tree.command(name="git_issue_create", description="Creates an issue.", guild=guild_id)
    @app_commands.check(is_admin)
    async def git_issue_create(interaction: discord.Interaction, title: str, body: str = ""):
        repo = grab_repo(git_client=git_client, repository=guild_git_repo)
        issue = open_issue(repo=repo, title=title, body=body, author=interaction.user.display_name)

        message = send_message(interaction=interaction, message=issue, local=False)
        await message

    @tree.command(name="embed", description="Embeds a message with given args.", guild=guild_id)
    @app_commands.check(is_admin)
    async def embed(interaction: discord.Interaction, title: str = None, description: str = None, colour: int = 15844367, thumbnail: str = "https://antistasiultimate.com/images/UACLogoSmall.png"):
        embed = format_embed(interaction=interaction, title=title, description=description, colour=colour, thumbnail=thumbnail)
        await interaction.response.send_message(embed=embed)
            
    @tree.command(name="changelog", description="Creates a changelog form using an embed.", guild=guild_id)
    @app_commands.check(is_admin)
    async def changelog(interaction: discord.Interaction, mod_type: Literal["Main", "Public Testing"]):
        await interaction.response.send_modal(changelog_modal(mod_type))

    @tree.command(name="shutdown_bot", description="Shuts down the bot.", guild=guild_id)
    @app_commands.check(is_admin)
    async def shutdown_bot(interaction: discord.Interaction, confirm: bool):
        if (confirm):
            log_message(-1, (f"{interaction.user.display_name} ({interaction.user.id}) is attempting shutdown."), header=guild_log_init, space=True)
            message = send_message(interaction=interaction, message=f"Shutting down the bot now.", local=False)
            await message

            await shutdown(client)
        else:
            message = send_message(interaction=interaction, message=f"Shutdown was not confirmed.", local=True)
            await message
            
    @tree.command(name="restart_bot", description="Restarts the bot, will fetch `main` from github first.", guild=guild_id)
    @app_commands.check(is_admin)
    async def restart_bot(interaction: discord.Interaction, confirm: bool):
        if (confirm):
            log_message(-1, (f"{interaction.user.display_name} ({interaction.user.id}) is attempting restart."), header=guild_log_init, space=True)
            message = send_message(interaction=interaction, message=f"Restarting the bot now.", local=False)
            await message

            # await shutdown(client)

            update_bot(client)
        else:
            message = send_message(interaction=interaction, message=f"Shutdown was not confirmed.", local=True)
            await message

    @tree.command(name="custom_message", description="Send a custom message.", guild=guild_id)
    @app_commands.check(is_admin)
    async def custom_message(interaction: discord.Interaction, text: str):
        message = send_message(interaction=interaction, message=f"User Message - {text}", local=False)
        await message

    @tree.command(name="send_latest_log", description="Sends the most recent log.", guild=guild_id)
    @app_commands.check(is_admin)
    async def send_latest_log(interaction: discord.Interaction):
        await send_log(client, interaction=interaction)

    @git_list.error
    @git_branch_update.error
    @git_pull_merge_ready.error
    @git_pull_merge.error
    @git_pull_create.error
    @git_issue_create.error
    @changelog.error
    @embed.error
    @shutdown_bot.error
    @custom_message.error
    @send_latest_log.error
    async def say_error(interaction : discord.Interaction, error):
        await send_message(interaction, error, local=True)
