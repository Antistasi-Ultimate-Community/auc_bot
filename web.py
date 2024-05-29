import requests
import discord

from config import url_missing
from config import guild_log_copyright
from log import log_message

#https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
def format_embed(interaction, title=None, description=None, type="rich", colour=15844367, thumbnail="https://antistasiultimate.com/images/UACLogoSmall.png"):

    log_message(-1, f"{interaction.user.name} ({interaction.user.id}) is sending an embedded message.", space=True)
    log_message(-1, f"Title: {title}")
    log_message(-1, f"Description: {description}")
    log_message(-1, f"Colour: {colour}")
    log_message(-1, f"Thumbnail: {thumbnail}")

    embed_message = discord.Embed(title=title, description=description, type=type, colour=colour)
    embed_message.set_thumbnail(url=thumbnail)
    embed_message.set_footer(text=guild_log_copyright)
    return embed_message

def send_changelog(interaction, mod_type="main", changelog={"version": "10.0.0", "changelog": ["Test", "URL"]}):
    log_message(-1, f"{interaction.user.name} ({interaction.user.id}) is sending a changelog embed.", space=True)
    log_message(-1, f"Mod Type: {mod_type}")
    log_message(-1, f"Changelog Version/URL: {changelog}")

    if (mod_type == "Public Testing"):
        colour = 16711680 #red
        target = "Antistasi Ultimate - Public Testing"
        target_url = "https://steamcommunity.com/sharedfiles/filedetails/?id=3169463443"
        thumbnail = "https://antistasiultimate.com/images/yellow_dev.png"
    else:
        colour = 15844367 #gold
        target = "Antistasi Ultimate - Mod"
        target_url = "https://steamcommunity.com/sharedfiles/filedetails/?id=3020755032"
        thumbnail = "https://antistasiultimate.com/images/Yellow.png"

    embed_message = format_embed(interaction=interaction, title="Antistasi Ultimate Update", colour=colour, thumbnail=thumbnail)
    embed_message_changelog = format_embed(interaction=interaction, title="Antistasi Ultimate Changelog", colour=colour, thumbnail=thumbnail)
    
    changelog_version = changelog["version"]
    changelog = changelog["changelog"]

    embed_message_changelog.add_field(name=f"Version: v{changelog_version}", value=f"```{changelog[0]}```\n[Full Changelog]({changelog[1]})")
    embed_message.add_field(name=f"Target: {target}\nVersion: v{changelog_version}", value=f"[Mod Link]({target_url})\n[Changelog Link]({changelog[1]})\n\nSee the changelog below.\n\nTo avoid issues, please repair the mod in your launcher.\nIf applicable, reinstall the mod to your server (Completely delete the mod first).")

    return interaction.response.send_message(embeds=[embed_message, embed_message_changelog])

def send_message(interaction, message, local=False):    
    try:
        if (local == False):
            log_message(-1, (f"{interaction.user.name} is sending a message: {message}"))
            
        return interaction.response.send_message(message, ephemeral=local)
    except: # should probably add a proper exception here
        log_message(-1, (f"Could not send message. {message}"))

def check_url(url=""): 
    try:
        response = requests.head(url)

        # check the status code
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        return e

def return_url(url="", suppress=False):
    url_exists = check_url(url)
    
    if (url_exists):
        if (suppress == True):
            url = f"<{url}>"
            log_message(-1, (f"{url} has been suppressed."))
        return url
    else:
        return False

def send_url(interaction, url, local=False, suppress=False):
    url_send = return_url(url=url, suppress=suppress)
    if (url_send != False):
        log_message(-1, (f"{interaction.user.name} is sending a url: {url_send}"))
        return send_message(interaction=interaction, message=url_send, local=False)
    else:
        log_message(-1, (f"{interaction.user.name} attempted to send a url, but it was 404: {url}"))
        return url_missing(interaction=interaction)