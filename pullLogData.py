import requests
import csv

url = 'https://api.github.com/repos/pytorch/pytorch/pulls'
owner = 'owner_name'
repo = 'repository_name'

response = requests.get(url.format(owner=owner, repo=repo))
pull_requests = response.json()

with open('pull_requests.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Created At', 'URL', 'Username'])
    for pr in pull_requests:
        writer.writerow([pr['title'], pr['created_at'], pr['html_url'], pr['user']['login']])