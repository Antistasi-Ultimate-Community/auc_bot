import discord

from handle_message import has_identifier
from handle_message_github import return_pull

# Should probably consider moving on_message to main.py and calling this function there
def handle_message(client):
    @client.event
    async def on_message(message):
        reply = ""
        if (message.author.id == client.user.id):
            return False

        content = message.content
        channel = message.channel

        is_pull = has_identifier(content, "##")
        if (is_pull):
            # Split all content that isn't related to a pull request index
            pull_index_filter = content.split(" ") 
            
            # Filter the resulting list to remove any elements that don't have the identifier
            index = [index for index in pull_index_filter if "##" in index][0]
            
            pull_index = index.split("##")[1]

            url = return_pull(pull_index=pull_index)

            reply = url

        if (reply != ""):
            await channel.send(reply)