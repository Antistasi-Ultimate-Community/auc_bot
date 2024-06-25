from config import git_client

from handle_message_github import return_pull

def grab_repo(git_client=None, repository=""):
    if (git_client == None):
        raise Exception(f"git_client returned {git_client}")

    if (repository == ""):
        repository = "SilenceIsFatto/A3-Antistasi-Ultimate"
        # raise Exception(f"repository returned {repository}, needs to be in format 'Owner/Repo'")

    repo = git_client.get_repo(repository)

    return repo

def grab_issues(git_client=None, type="issue"):

    print(type)

    repo = grab_repo(git_client=git_client)

    issues = {}

    text = ""

    repo_issues_open = repo.get_issues(state="open")

    for issue in repo_issues_open:
        title = issue.title
        number = issue.number

        url = return_pull(number)

        print(url)

        if ("issues" in url and type != "issue"):
            continue

        if ("pull" in url and type != "pull"):
            continue

        text = f"{text}\n{title} - [#{number}](<{url}>)\n"

        print(number, title)

        issues[issue] = {"number": number, "title": title}


    return [issues, text]