import subprocess

from config import guild_git_repo_normal
from config import guild_git_repo_debug
from config import guild_git_repo_bot

import os
import sys

from config import shutdown

def git_pull(repository=""):
    # pull from remote origin to the current working dir:

    repo = f"{repository}.git"
    output = subprocess.check_output(["git", "pull", "--rebase"])

    print(output)

def update_bot(client):

    git_pull(guild_git_repo_bot)

    os.execl(sys.executable, "python", "main.py")

if (__name__ == "__main__"):
    git_pull(guild_git_repo_bot)