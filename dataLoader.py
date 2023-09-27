from datetime import datetime

timestamp_str = '2023-09-01 00:00:00+05:30'
timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S%z')
print(timestamp)