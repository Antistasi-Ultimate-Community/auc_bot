import discord

from handle_message import identifier_is_github
from handle_message import identifier_github
from handle_message_github import return_pull

from config import guild_channel_bot
from config import grab_exempt_channels

from log import log_message
from log_discord import log_message_channel

# Should probably consider moving on_message to main.py and calling this function there
def handle_message(client):
    @client.event
    async def on_message(message):
        reply = None
        embed = None

        guild_channel_log = client.get_channel(guild_channel_bot)

        guild_channel_log_exempt = client.get_channel(guild_channel_bot)
        author = message.author
        author_id = message.author.id
        author_name = message.author.name
        client_id = client.user.id
        content = message.content
        channel = message.channel

        # Ideally we shouldn't be running grab_exempt_channels each time a message is sent, but caching isn't viable rn
        if (channel in grab_exempt_channels(client)):
            return False

        if (author_id == client_id):
            return False

        if (content == "" or content == None):
            return False

        if (identifier_is_github(content=content)):
            reply = identifier_github(content=content)

        log_message(-1, f"{author_name}: {content} ({channel})")
        embed = log_message_channel(message=content, author=author, channel=channel)

        if (reply != None):
            await channel.send(reply)

        if (embed != None):
            await guild_channel_log.send(embed=embed)