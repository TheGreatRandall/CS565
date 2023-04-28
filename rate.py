import requests

# function to get the total number of pull requests for a user


def get_total_pull_requests(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url)
    repos = response.json()
    total_pull_requests = 0
    for repo in repos:
        repo_name = repo["name"]
        url = f"https://api.github.com/repos/{user}/{repo_name}/pulls"
        response = requests.get(url)
        pulls = response.json()
        total_pull_requests += len(pulls)
    return total_pull_requests

# function to get the number of accepted pull requests for a user


def get_accepted_pull_requests(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url)
    repos = response.json()
    accepted_pull_requests = 0
    for repo in repos:
        repo_name = repo["name"]
        url = f"https://api.github.com/repos/{user}/{repo_name}/pulls?state=closed"
        response = requests.get(url)
        pulls = response.json()
        for pull in pulls:
            if pull["merged_at"] is not None:
                accepted_pull_requests += 1
    return accepted_pull_requests


# example usage
user = input("Enter your Github username: ")
total_pull_requests = get_total_pull_requests(user)
accepted_pull_requests = get_accepted_pull_requests(user)
print(f"User {user} has {total_pull_requests} total pull requests and {accepted_pull_requests} accepted pull requests.")
