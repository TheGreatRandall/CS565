import requests
import csv
import random
import time

headers = {
    'Authorization': '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',
    'Accept': 'application/vnd.github+json'
}


def fetch_data(url, params=None):
    while True:
        response = requests.get(url, headers=headers, params=params)
        remaining_rate_limit = int(
            response.headers.get('X-RateLimit-Remaining', 0))
        rate_limit_reset_time = int(
            response.headers.get('X-RateLimit-Reset', time.time()))

        if response.status_code != 200:
            print("Error fetching data:", response.status_code, response.text)
            if remaining_rate_limit <= 1:
                sleep_time = rate_limit_reset_time - time.time() + 5  # Adding 5 seconds buffer
                print(
                    f"Rate limit exceeded, waiting for {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                time.sleep(60)  # Sleep for 60 seconds
            continue

        return response


def fetch_merged_prs():
    url = 'https://api.github.com/repos/pytorch/pytorch/pulls'
    params = {
        'state': 'closed',
        'per_page': 100,
        'page': 1
    }

    merged_users = set()

    while True:
        response = fetch_data(url, params=params)
        data = response.json()

        if not data or not isinstance(data, list):
            break

        for pr in data:
            if 'user' not in pr or 'login' not in pr['user']:
                continue

            if pr['merged_at'] is not None:
                merged_users.add(pr['user']['login'])

        params['page'] += 1

    return merged_users


def fetch_rejected_prs():
    url = 'https://api.github.com/repos/pytorch/pytorch/pulls'
    params = {
        'state': 'closed',
        'per_page': 100,
        'page': 1
    }

    rejected_users = set()

    while True:
        response = fetch_data(url, params=params)
        data = response.json()

        if not data or not isinstance(data, list):
            break

        for pr in data:
            if 'user' not in pr or 'login' not in pr['user']:
                continue

            if pr['merged_at'] is None:
                rejected_users.add(pr['user']['login'])

        params['page'] += 1

    return rejected_users


def fetch_contributors():
    url = 'https://api.github.com/repos/pytorch/pytorch/contributors'
    params = {
        'per_page': 100,
        'page': 1
    }

    contributors = set()

    while True:
        response = fetch_data(url, params=params)
        data = response.json()

        if not data or not isinstance(data, list):
            break

        for contributor in data:
            if 'login' not in contributor:
                continue

            contributors.add(contributor['login'])

        params['page'] += 1

    return contributors


active_users = fetch_merged_prs()
rejected_users = fetch_rejected_prs()
contributors = fetch_contributors()
inactive_users = random.sample(
    rejected_users + list(set(contributors) - active_users), len(active_users))

with open('user_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['user', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
