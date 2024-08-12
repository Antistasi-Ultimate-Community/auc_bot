import discord
from discord.ext import commands
from discord import app_commands

import os

import logging

from bot_token import token
from config import guild_id
from config import guild_log_file
from config import guild_log_init
from config import guild_name_bot

from config import guild_roles_admin
from config import guild_roles_moderator
from config import guild_roles_log_exempt
from config import guild_channel_player_count

from events import handle_message

from log import log_message

from commands import commands_init

from config import git_client

from steam_server import grab_server

from presence import presence_loop
from presence import presence_loop_thread

import asyncio

# import signal
# import sys

if not os.path.exists("logs"):
    os.makedirs("logs")

handler = logging.FileHandler(filename=guild_log_file, encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

# def signal_handler(signal, frame):
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

# May be useful in future ^

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        try:
            await self.wait_until_ready()

            log_message(-1, message=f'We have logged into Discord as {client.user}. ID: {client.user.id}\n', header=guild_log_init, space=True)
            log_message(-1, message=f"Admin Roles: {guild_roles_admin}\nModerator Roles: {guild_roles_moderator}\nExempt Roles: {guild_roles_log_exempt}")

            if not self.synced:
                await tree.sync(guild=guild_id)
                self.synced = True
        except:
            log_message(-1, ("Something went wrong!"))

        await asyncio.create_task(presence_loop(client=client))
        
client = aclient()
tree = commands_init(client)

handle_message(client)
client.run(token, log_handler=handler)

git_client.close()