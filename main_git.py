from github import Github
from github import Auth

def start_git_client(github_login=None):

    if (github_login == None or github_login == ""):
        print("No github login was given. Github features will be unavailable!")
        return None

    # Do note, if not using a token, some features may not work
    if (isinstance(github_login, str)):
        auth = Auth.Token(github_login)
    else:
        auth = Auth.Login(github_login[0], github_login[1])
        print(f"We have logged into Github as {github_login[0]}.\n")

    # Public Web Github
    git_client = Github(auth=auth)

    return git_client

if (__name__ == "__main__"):
    git_client = start_git_client()