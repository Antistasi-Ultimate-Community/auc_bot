from config import git_client
from config import guild_log_file
from config import pull_request_template

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

def grab_pulls_merge_ready(git_client=None, repo=None):

    if (repo == None):
        repo = grab_repo(git_client=git_client)

    pulls_merge = {}
    pulls_merge_numbers = []

    pulls = repo.get_pulls(state='open', sort='created')
    for pull in pulls:
        pull_labels = pull.get_labels()
        for label in pull_labels:
            label_name = label.name
            if (label_name == "ready-for-merge"):
                title = pull.title
                number = pull.number

                pulls_merge[pull] = {"number": number, "title": title}
                pulls_merge_numbers.append(number)

    return [pulls_merge, pulls_merge_numbers]

def grab_issues(git_client=None, type=None, repo=None):

    if (type == None):
        raise Exception(f"type returned {type}")

    if (repo == None):
        repo = grab_repo(git_client=git_client)

    text = ""
    issues = {}

    repo_issues_open = repo.get_issues(state="open")

    repo_issues = [issue for issue in repo_issues_open if issue.pull_request == None]
    repo_pulls = [issue for issue in repo_issues_open if issue.pull_request != None]

    if (type == "issues"):
        issues_list = repo_issues
    else:
        issues_list = repo_pulls

    for issue in issues_list:
        title = issue.title
        number = issue.number

        url = f"https://github.com/{repo.full_name}/{type}/{number}"

        text = f"{text}\n{title} - [#{number}](<{url}>)\n"

        issue_labels = issue.get_labels()

        labels = []

        for label in issue_labels:
            # if (label.name == "ready-for-merge"):
            labels.append(label.name)

        text = f"{text} - Labels: {labels}\n"

        print(number, title)

        issues[issue] = {"number": number, "title": title}


    return [issues, text]

def open_issue(repo=None, title=None, body=None, author=None):
    if (title == None):
        raise Exception("Creating an issue requires a title. Please give one and try again!")

    if (author == None):
        author = "AUC#7708"

    body = f"This is an auto-generated issue from {author} (Discord).\n\n{body}"

    issue = repo.create_issue(title=title, body=body)

    issue_link = f"https://github.com/{repo.full_name}/issues/{issue.number}"

    message = f"Created `{title}` (#{issue.number}).\n[Link]({issue_link})"

    return message

def open_pull(repo=None, base=None, head=None, title=None, body=None, author=None):
    if (base == None or head == None):
        raise Exception("Creating a pull request requires a base and head branch. Please provide them and try again!")

    if (title == None or title == ""):
        title = f"Automated PR ({base} << {head})"

    if (author == None):
        author = "AUC#7708"

    if (body == None or body == ""):
        body = f"**_This is an auto-generated pull request from {author} (Discord)._**"

    body = f"{body}\n{pull_request_template}"

    title = f"[BOT] {title}"

    pull = repo.create_pull(base=base, head=head, title=title, body=body)

    pull_link = f"https://github.com/{repo.full_name}/pull/{pull.number}"

    message = f"Created `{title}` (#{pull.number}).\n[Link]({pull_link})"

    return message

def merge_pull(repo=None, number=None, merge_method="merge"):
    pull_request = repo.get_pull(number)
    pull_link = f"https://github.com/{repo.full_name}/pull/{pull_request.number}"

    try:
        merge = pull_request.merge(merge_method=merge_method)
    
    except:
        message = f"[X] Something failed whilst merging `{pull_request.title}` (#{number}). - [It was aborted.]({pull_link})\nPerhaps the pull request was already merged/closed or has a merge conflict?"

        return message

    message = f"Merged `{pull_request.title}` (#{pull_request.number}).\n[Link](<{pull_link}>)"

    return message

def merge_pulls(repo=None, numbers=None):
    if (numbers == None):
        raise Exception(f"numbers returned {numbers}")

    if (numbers == [] or len(numbers) == 0):
        message = f"No pull requests are ready for merge."

        return message

    pulls_merged_num = 0

    message = ""

    for number in numbers:
        pull_message = merge_pull(repo=repo, number=number)
        message = f"{message}\n\n{pull_message}"
        if ("[X]" not in message):
            pulls_merged_num += 1

    message = f"{message}\n\nMerged {pulls_merged_num} pulls.\n"

    return message

def update_branch(repo=None, base=None, head=None):
    if (base == None):
        raise Exception("Updating a branch requires a base branch. Please provide one and try again!")

    if (base == "unstable"):
        raise Exception("Unstable is not allowed as the base branch. Perhaps you meant to use it as the head branch?")

    if (head == None):
        head = "unstable"

    branch_head = repo.get_branch(branch=head)

    try:

        commit = repo.merge(base, branch_head.commit.sha, f"Merge {head} into {base}. [UPDATE]")

        message = f"Updated `{base}` with `{head}`."

    except:
        message = f"You'll have to do this manually, auto merge failed. Possibly a merge conflict?"

        return message