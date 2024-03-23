import requests
import json

root_url = 'https://gitlab.com/api/v4/projects/54360847'
gitlab_ids = {"Nirmal": 15538898, "Adrian": 15580304,
              "Alec": 15573017, "Junyu": 15554133}

# Get commits for each project member
def getCommits(root_url, gitlab_ids):
    url = root_url + '/repository/commits'
    params = {"per_page": 100, "page": 1}
    commit_tracker = {"Nirmal": 0, "Adrian": 0, "Alec": 0, "Junyu": 0}
    commits = []

    response = requests.get(url, params=params)
    page_commits = response.json()

    while page_commits:
        commits.extend(page_commits)
        params["page"] += 1
        response = requests.get(url, params=params)
        page_commits = response.json()

    for commit in commits:
        author = commit["author_name"].split()[0]
        if author == "nirmpatel":
            author = "Nirmal"
        if author in gitlab_ids:
            commit_tracker[author] += 1

    return commit_tracker

# Get issues for each project member
def getIssues(root_url, gitlab_ids):
    url = root_url + '/issues_statistics?author_id='
    issue_tracker = {'Nirmal': 0, 'Adrian': 0, 'Alec': 0, 'Junyu': 0}

    for key, ID in gitlab_ids.items():
        url_temp = url + str(ID)
        response = requests.get(url_temp)
        data = json.loads(response.content)

        issue_tracker[key] = data["statistics"]["counts"]["all"]

    return issue_tracker

# print(getCommits(root_url, gitlab_ids))
# print(getIssues(root_url, gitlab_ids))
