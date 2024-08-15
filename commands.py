import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from commands_admin import commands_admin
from commands_moderator import commands_moderator

from config import guild_id

from log import log_message

from mg_init import init
from mg_map import return_map, grab_map_names, grab_maps, link_to_map, map_to_embed

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

        modset_message = init(modsets=modsets, climates=climates, era=era, key=key, dlc=dlc, double_occ=double_occ, simple=simple)

        embeds = []
        embed = format_embed(interaction=interaction, title="Modset Generator - Factions", description=modset_message)
        embeds.append(embed)

        # move this to its own function and do basically the same thing as factions, validate climates etc and return accordingly
        map_file = None
        
        if (map_file == None):
            message = interaction.response.send_message(embeds=embeds, ephemeral=local)
        else:
            message = interaction.response.send_message(file=map_file, embeds=embeds, ephemeral=local)

        await message

    @tree.command(name="map", description="Sends a 1024x1024 image of a map. You can use a steam workshop link instead of a name.", guild=guild_id)
    async def map(interaction: discord.Interaction, map_name: str, local: bool = True):

        if ("http" in map_name):
            map_name = link_to_map(map_name)
        
        if (type(map_name) is not list):
            # move this to its own function
            map_return = map_to_embed(map_name, interaction)

            map_file = map_return[0]
            embed = map_return[1]

            message = interaction.response.send_message(file=map_file, embed=embed, ephemeral=local)
        else:
            embeds = []
            map_files = []

            map_names = map_name
            for map_name in map_names:

                map_return = map_to_embed(map_name, interaction)

                map_file = map_return[0]
                embed = map_return[1]

                map_files.append(map_file)
                embeds.append(embed)

            message = interaction.response.send_message(files=map_files, embeds=embeds, ephemeral=local)

        await message

    @tree.command(name="maps", description="Sends a list of supported map names.", guild=guild_id)
    async def maps(interaction: discord.Interaction, local: bool = True):
        
        map_names = grab_map_names()

        map_description = "\n".join(map_names)

        embed = format_embed(interaction=interaction, title="Map Names", description=map_description)
        embed.set_footer(text=f"{len(map_names)} maps are supported. Use /map with one of these names for more info!")
            
        message = interaction.response.send_message(embed=embed, ephemeral=local)
        await message

    @generate_modset_help.error
    @generate_modset.error
    @map.error
    @maps.error
    async def say_error(interaction : discord.Interaction, error):
        await send_message(interaction, error, local=True)

    return tree