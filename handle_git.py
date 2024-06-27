from config import git_client
from config import guild_log_file

from handle_message_github import return_pull

from file_operations import write_to_file

def git_logged_in(git_client=None):
    if (git_client != None):
        return True
    else:
        return False

def grab_repo(git_client=None, repository=""):
    if (git_client == None):
        raise Exception(f"git_client returned {git_client}")

    if (repository == ""):
        repository = "SilenceIsFatto/A3-Antistasi-Ultimate"
        # raise Exception(f"repository returned {repository}, needs to be in format 'Owner/Repo'")

    repo = git_client.get_repo(repository)

    return repo

def grab_issues(git_client=None, type=None):

    if (type == None):
        raise Exception(f"type returned {type}")

    repo = grab_repo(git_client=git_client)

    text = ""
    issues = {}

    repo_issues_open = repo.get_issues(state="open")

    repo_issues = [issue for issue in repo_issues_open if issue.pull_request == None]
    repo_pulls = [issue for issue in repo_issues_open if issue.pull_request != None]

    # write_to_file(guild_log_file, repo_issues)
    # write_to_file(guild_log_file, repo_pulls)

    if (type == "issues"):
        issues_list = repo_issues
    else:
        issues_list = repo_pulls

    for issue in issues_list:
        title = issue.title
        number = issue.number

        # url = return_pull(number)

        url = f"https://github.com/{repo.full_name}/{type}/{number}"

        text = f"{text}\n{title} - [#{number}](<{url}>)\n"

        print(number, title)

        issues[issue] = {"number": number, "title": title}


    return [issues, text]

def open_issue(repo=None, title=None):
    if (title == None):
        raise Exception("Creating an issue requires a title. Please give one and try again!")

    issue = repo.create_issue(title=title, body="This is an auto-generated issue from AUC#7708 (Discord).")

    issue_link = f"https://github.com/{repo.full_name}/issues/{issue.number}"

    message = f"Created `{title}` (#{issue.number}).\n[Link]({issue_link})"

    return message

def open_pull(repo=None, base=None, head=None, title=None, body=None):
    if (base == None or head == None):
        raise Exception("Creating a pull request requires a base and head branch. Please provide them and try again!")

    if (title == None or title == ""):
        title = f"Automated PR ({base} << {head})"

    if (body == None or body == ""):
        body = f"This is an auto-generated pull request from AUC#7708 (Discord)."

    title = f"[BOT] {title}"

    pull = repo.create_pull(base=base, head=head, title=title, body=body)

    pull_link = f"https://github.com/{repo.full_name}/pull/{pull.number}"

    message = f"Created `{title}` (#{pull.number}).\n[Link]({pull_link})"

    return message

def merge_pull(repo=None, number=None):
    try:
        pull_request = repo.get_pull(number)

        merge = pull_request.merge()
    
    except:
        message = f"Something went wrong. Perhaps the pull request was already merged/closed?"

        return message

    pull_link = f"https://github.com/{repo.full_name}/pull/{pull_request.number}"

    message = f"Merged `{pull_request.title}` (#{pull_request.number}).\n[Link]({pull_link})"

    return message

def update_branch(repo=None, base=None, head=None):
    if (base == None):
        raise Exception("Updating a branch requires a base branch. Please provide one and try again!")

    if (head == None):
        head = "unstable"

    branch_head = repo.get_branch(branch=head)

    try:

        commit = repo.merge(base, branch_head.commit.sha, f"Merge {head} into {base}. [UPDATE]")

        message = f"Updated `{base}` with `{head}`."

    except:
        message = f"You'll have to do this manually, auto merge failed. Possibly a merge conflict?"

        return message

    return message