import subprocess

from config import guild_git_repo_normal
from config import guild_git_repo_debug
from config import guild_git_repo_bot

import os
import sys

from config import shutdown

def install_library(name):
    print(f"Installing library: {name}")
    subprocess.call([sys.executable, '-m', 'pip', 'install', name])

def install_libraries(file=None):
    if (file == None):
        raise Exception("A file is needed to run this function.")

    with open(file) as requirements:
        lines = requirements.readlines()

        for line in lines:
            requirement = line.strip()

            install_library(requirement)

def git_pull(repository=""):
    repo = f"{repository}.git"
    output = subprocess.check_output(["git", "pull", "--rebase"])

    print(output)

def restart_bot(client, pull=False):

    if (pull):
        git_pull(guild_git_repo_bot)

        install_libraries("requirements.txt")

    os.execl(sys.executable, "python", "main.py")

if (__name__ == "__main__"):
    git_pull(guild_git_repo_bot)