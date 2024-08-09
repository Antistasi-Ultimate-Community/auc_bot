import discord

from handle_message import identifier_is_github
from handle_message import identifier_github
from handle_message_github import return_pull

from config import guild_channel_bot
from config import grab_exempt_channels
from config import guild_user_webhook_id

from webhooks import recieve_webhook

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
        content = message.content
        channel = message.channel
        message_link = message.jump_url

        client_id = client.user.id

        # Ideally we shouldn't be running grab_exempt_channels each time a message is sent, but caching isn't viable rn
        if (channel in grab_exempt_channels(client)):
            return False

        if (author_id == client_id):
            return False

        if (content == "" or content == None):
            return False

        if (author_id in [guild_user_webhook_id, 474144080801169418]):
            print(f"Webhook recieved from {author_name}")

            recieve_webhook(content=content, author_id=author_id)

        if (identifier_is_github(content=content)):
            reply = identifier_github(content=content)

        log_message(-1, f"{author_name}:\n{content} ({channel})")
        embed = log_message_channel(message=content, author=author, channel=channel, message_link=message_link)

        if (reply != None):
            await channel.send(reply)

        if (embed != None):
            await guild_channel_log.send(embed=embed)