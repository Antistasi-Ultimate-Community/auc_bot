import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from commands_admin import commands_admin
from commands_moderator import commands_moderator

from config import guild_id

from log import log_message

from mg_init import init

from typing import Literal

from web import send_message
from web import format_embed

def commands_init(client):

    tree = app_commands.CommandTree(client)

    commands_admin(client, tree)
    commands_moderator(client, tree)

    @tree.command(name="generate_modset_help", description="Shows all of the parameters for generate_modset.", guild=guild_id)
    async def generate_modset_help(interaction: discord.Interaction):
        help_message = "# USE A COMMA (,) BETWEEN EACH PARAMETER, AND DON'T USE SPACES.\nhttps://github.com/Antistasi-Ultimate-Community/auc_bot/wiki/Modset-Generator"
        message = send_message(interaction=interaction, message=help_message, local=True)
        await message

    @tree.command(name="generate_modset", description="Generates a modset with given parameters.", guild=guild_id)
    async def generate_modset(interaction: discord.Interaction, modsets: str, climates: str = "", era: Literal["modern", "scifi", "lowtech", "coldwar", "stalker"] = "", key: Literal["vanilla", "rhs"] = "", dlc: str = "", double_occ: bool = False, simple: bool = True, local: bool = True):
        modsets = modsets.split(",")
        climates = climates.split(",")
        dlc = dlc.split(",")
        log_msg = f"{interaction.user.display_name} ({interaction.user.id}) is generating a modset."
        log_message(-1, log_msg)

        modset_message = init(modsets=modsets, climates=climates, era=era, key=key, dlc=dlc, double_occ=double_occ, simple=simple)
        embed = format_embed(interaction=interaction, title="Modset Generator", description=modset_message)
        message = interaction.response.send_message(embed=embed, ephemeral=local)
        # message = send_message(interaction=interaction, message=modset_message, local=False)
        await message

    @tree.command(name="map_image", description="Sends a 1024x1024 image of a map.", guild=guild_id)
    async def map_image(interaction: discord.Interaction, map_name: str, local: bool = False):

        map_name_formatted = f"{map_name}.jpg"

        map_file = discord.File(f"images/maps/{map_name_formatted}")

        embed = format_embed(interaction=interaction, title=map_name, description=None)
        embed.set_image(url=f"attachment://{map_name_formatted}")

        message = interaction.response.send_message(file=map_file, embed=embed, ephemeral=local)
        await message

    @generate_modset_help.error
    @generate_modset.error
    @map_image.error
    async def say_error(interaction : discord.Interaction, error):
        await send_message(interaction, error, local=True)

    return tree