import requests
import csv

# Replace YOUR_GITHUB_TOKEN with your personal GitHub access token
headers = {
    'Authorization': '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',
    'Accept': 'application/vnd.github+json'
}

url = 'https://api.github.com/repos/pytorch/pytorch/pulls?state=closed'
params = {
    'state': 'closed',
    'per_page': 100,
    'page': 1
}

# Fetch the data and store it in a list
pr_data = []
while True:
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if not data or not isinstance(data, list):
        break

    for pr in data:
        if 'user' not in pr or 'login' not in pr['user']:
            continue

        pr_data.append({
            'user': pr['user']['login'],
            'date': pr['created_at'],
            'merged': 'T' if pr['merged_at'] is not None else 'F'
        })

    params['page'] += 1

# Write the data to a CSV file
with open('pr_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['user', 'date', 'merged']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for pr in pr_data:
        writer.writerow(pr)

print("CSV file generated successfully.")
