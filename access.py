import discord

from config import guild_roles_moderator
from config import guild_channel_bot

def is_moderator(interaction: discord.Interaction):
    if (interaction.user.id == 474144080801169418):
        return True

    roles = interaction.user.roles
    for role in roles:
        if (role.id in guild_roles_moderator):
            return True
        else:
            continue

        return False

def is_channel_bot(interaction: discord.Interaction):
    if (is_moderator):
        return True

    channel_id = interaction.channel.id

    # if (guild_channel == 0):
    #     return False

    if (channel_id == guild_channel_bot):
        return True
    else:
        return False