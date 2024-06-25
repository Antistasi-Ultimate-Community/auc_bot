from github import Github
from github import Auth

from bot_token import github_login

def start_git_client():

    auth = Auth.Login(github_login[0], github_login[1])

    # Public Web Github
    git_client = Github(auth=auth)

    return git_client

if (__name__ == "__main__"):
    git_client = start_git_client()