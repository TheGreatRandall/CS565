import os
import requests
import csv
import random
import time

headers = {
    'Authorization': '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',
    'Accept': 'application/vnd.github+json'
}

# Fetch merged PRs (active users)


def fetch_merged_prs():
    url = 'https://api.github.com/repos/pytorch/pytorch/pulls?state=closed'
    params = {'page': 1}

    active_users = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching data:", response.status_code, response.text)
            time.sleep(60)  # Sleep for 60 seconds
            continue

        data = response.json()

        if not data or not isinstance(data, list):
            break

        for pr in data:
            if 'user' not in pr or 'login' not in pr['user']:
                continue
            if pr['merged_at'] is not None:
                active_users.append(pr['user']['login'])

        params['page'] += 1

    return active_users

# Fetch closed but not merged PRs (rejected PRs)


def fetch_rejected_prs():
    url = 'https://api.github.com/repos/pytorch/pytorch/pulls?state=closed'
    params = {'page': 1}

    rejected_users = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching data:", response.status_code, response.text)
            time.sleep(60)  # Sleep for 60 seconds
            continue

        data = response.json()

        if not data or not isinstance(data, list):
            break

        for pr in data:
            if 'user' not in pr or 'login' not in pr['user']:
                continue
            if pr['merged_at'] is None:
                rejected_users.append(pr['user']['login'])

        params['page'] += 1

    return rejected_users

# Fetch a list of contributors from the repository (to generate random users)


def fetch_contributors():
    url = 'https://api.github.com/repos/pytorch/pytorch/contributors'
    params = {'page': 1}

    contributors = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching data:", response.status_code, response.text)
            time.sleep(60)  # Sleep for 60 seconds
            continue

        data = response.json()

        if not data or not isinstance(data, list):
            break

        for user in data:
            if 'login' not in user:
                continue
            contributors.append(user['login'])

        params['page'] += 1

    return contributors


def main():
    active_users = fetch_merged_prs()
    rejected_users = fetch_rejected_prs()
    contributors = fetch_contributors()

    # Calculate the number of inactive users needed based on active users count
    num_inactive_users_needed = len(active_users)

    # Create a set of inactive users
    inactive_users_set = set(
        rejected_users + list(set(contributors) - set(active_users)))

    # Adjust the sample size to the minimum of the desired ratio and the actual population size
    num_inactive_users = min(num_inactive_users_needed,
                             len(inactive_users_set))

    # Generate the final list of inactive users
    inactive_users = random.sample(inactive_users_set, num_inactive_users)

    # Write the data to a CSV file
    with open('user_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['user', 'is_active']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user in active_users:
            writer.writerow({'user': user, 'is_active': 'T'})
        for user in inactive_users:
            writer.writerow({'user': user, 'is_active': 'F'})

    print("CSV file generated successfully.")


if __name__ == "__main__":
    main()
