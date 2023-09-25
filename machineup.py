import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import numpy as np


# last hr time
# last_hour_date_time = datetime.now() - timedelta(minutes= 1)
# lh_time = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

# print(lh_time)

# df = pd.read_csv('new.csv')

# for index,row in df.iterrows():
#     print(row['lastuv_inspectionOn'])


import numpy as np

# Example datetime with milliseconds and timezone
datetime_with_ms = np.datetime64('2023-09-23 17:34:20.580102')

# Remove milliseconds and timezone
datetime_without_ms = datetime_with_ms.astype('datetime64[s]')
formatted_datetime = str(datetime_without_ms).replace('T', ' ')[:-3]
# Print the result
print(formatted_datetime)
