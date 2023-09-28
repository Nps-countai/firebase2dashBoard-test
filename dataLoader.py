from datetime import datetime,timedelta

# last hr time
ct = datetime.now()
last_hour_date_time = datetime.now() - timedelta(minutes= 5)
lh_time = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
ct = ct.strftime('%Y-%m-%d %H:%M:%S')
# timestamp = datetime.strptime(lh_time, '%Y-%m-%d %H:%M:%S')
print(type(ct), type(lh_time))
print((ct)>(lh_time))
