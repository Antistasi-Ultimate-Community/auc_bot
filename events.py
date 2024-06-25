import discord

from handle_message import has_identifier
from handle_message_github import return_pull

from config import guild_channel_bot

from log import log_message
from log_discord import log_message_channel

# Should probably consider moving on_message to main.py and calling this function there
def handle_message(client):
    @client.event
    async def on_message(message):
        reply = None
        embed = None

        guild_channel_log = client.get_channel(guild_channel_bot)
        author = message.author
        author_id = message.author.id
        author_name = message.author.name
        client_id = client.user.id
        content = message.content
        channel = message.channel

        if (author_id == client_id):
            return False

        log_message(-1, f"{author_name}: {content} ({channel})")
        embed = log_message_channel(message=content, author=author, channel=channel)

        # Put in own function eventually, to clean this file up a bit
        is_pull = has_identifier(content, "##")
        if (is_pull):
            # Split all content that isn't related to a pull request index
            pull_index_filter = content.split(" ") 
            
            # Filter the resulting list to remove any elements that don't have the identifier
            index = [index for index in pull_index_filter if "##" in index][0]
            
            pull_index = index.split("##")[1]

            url = return_pull(pull_index=pull_index)

            reply = url

        if (reply != None):
            await channel.send(reply)

        if (embed != None):
            await guild_channel_log.send(embed=embed)