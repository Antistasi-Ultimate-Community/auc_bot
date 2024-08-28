from threads import thread_function

from steam_server import grab_server

from config import guild_channel_player_count

import discord

import asyncio

async def presence_loop(client=None):
    if (client == None):
        raise Exception("Client not found.")
        
    print("Starting presence loop.")
    channel_player = client.get_channel(guild_channel_player_count)
    while (True):

        print("Setting new presence.")
        
        server = grab_server()

        server_info = server[0]

        if (server_info == False):
            server_name = "Unavailable"
            player_count = 0
            player_count_max = 0
        else:
            server_name = server_info.server_name
            player_count = server_info.player_count
            player_count_max = server_info.max_players

            if (server_name == "Antistasi Ultimate Community Server 3"):
                server_name = "AUC Server 3"

            if (server_name == "Antistasi Ultimate Community Server 2"):
                server_name = "AUC Server 2"

            if (server_name == "Antistasi Ultimate Community Server 1"):
                server_name = "AUC Server 1"

        player_count_formatted = f"{server_name}: {player_count}/{player_count_max}"

        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=player_count_formatted))
        await channel_player.edit(name=player_count_formatted)

        await asyncio.sleep(120) # 2 mins

def presence_loop_thread_async(client=None):
    asyncio.run(presence_loop(client))

def presence_loop_thread(client=None):
    if (client == None):
        raise Exception("Client not found.")
         
    thread_function(target=presence_loop_thread_async, args=[client], start_thread=True)