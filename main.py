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

from events import handle_message

from file_operations import write_to_file

from log import log_message

from commands import commands_init

if not os.path.exists("logs"):
    os.makedirs("logs")

handler = logging.FileHandler(filename=guild_log_file, encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        try:
            await self.wait_until_ready()

            log_message(-1, message=f'We have logged in as {client.user}. ID: {client.user.id}\n', header=guild_log_init, space=True)

            if not self.synced:
                await tree.sync(guild=guild_id)
                self.synced = True
        except:
            log_message(-1, ("Something went wrong!"))

client = aclient()
tree = commands_init(client)

handle_message(client)

client.run(token, log_handler=handler)

os.system("cls")