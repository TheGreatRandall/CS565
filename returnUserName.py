import pandas as pd

# read pull_requests.csv file with ISO-8859-1 encoding
df = pd.read_csv('pull_requests.csv', encoding='ISO-8859-1')

# limit the number of rows to 100
df = df.head(100)

# drop duplicates based on username column
df.drop_duplicates(subset='Username', inplace=True)

# write the restored username to another csv file
df.to_csv('restored_usernames.csv', index=False, columns=['Username'])
