"""API and stats for GitLab activity"""


import requests
import json

gitlab_url = "https://gitlab.com"
group_id = 81639866
gitlab_members = {"Nirmal": 15538898, "Adrian": 15580304,
                  "Alec": 15573017, "Junyu": 15554133}


def get_commit_counts_per_project(project_id, commit_tracker):
    url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits"
    params = {"per_page": 100, "page": 1}
    response = requests.get(url, params=params)
    page_commits = response.json()
    while page_commits:
        for commit in page_commits:
            if "Merge branch" not in commit["message"]:
                author = commit["author_name"].split()[0]
                if author == "nirmpatel":
                    author = "Nirmal"
                if author in commit_tracker:
                    commit_tracker[author] += 1
        params["page"] += 1
        response = requests.get(url, params=params)
        page_commits = response.json()
    return commit_tracker


def get_commit_counts(group_id, gitlab_members):
    commit_tracker = {name: 0 for name in gitlab_members}
    url = f"{gitlab_url}/api/v4/groups/{group_id}/projects"
    response = requests.get(url)
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            project_id = project["id"]
            commit_tracker = get_commit_counts_per_project(
                project_id, commit_tracker)
    else:
        for name in commit_tracker:
            commit_tracker[name] = -1
    return commit_tracker


def get_issue_counts(group_id, gitlab_members):
    issue_tracker = {name: 0 for name in gitlab_members}
    url = f"{gitlab_url}/api/v4/groups/{group_id}/issues_statistics?author_id="
    for name in gitlab_members:
        member_url = url + str(gitlab_members[name])
        response = requests.get(member_url)
        data = json.loads(response.content)
        if response.status_code == 200:
            issue_tracker[name] = data["statistics"]["counts"]["all"]
        else:
            for name in issue_tracker:
                issue_tracker[name] = -1
            break
    return issue_tracker


commit_counts = get_commit_counts(group_id, gitlab_members)
issue_counts = get_issue_counts(group_id, gitlab_members)

# print(commit_counts)
# print(issue_counts)
