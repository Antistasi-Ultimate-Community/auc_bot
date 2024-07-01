import discord

from web import format_embed

from config import guild_roles_log_exempt

def log_message_channel(message=None, author=None, channel=None, message_link=None):
    if (isinstance(author, discord.User)):
        return None

    author_roles = author.roles
    author_name = author.name
    author_display_name = author.display_name
    author_avatar = author.avatar

    for role in author_roles:
        if (role.id in guild_roles_log_exempt):
            return None

    footer = f"{channel.id}"

    title = f"{author_display_name} ({author_name}) | #{channel}"

    message = f"{message}\n[Link]({message_link})"

    embed = format_embed(author=author, title=title, description=message, thumbnail=author_avatar, footer=footer, colour=9807270)
    
    return embed