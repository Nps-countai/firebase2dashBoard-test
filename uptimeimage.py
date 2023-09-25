import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings("ignore")




def imageGenerator():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('log.csv')

    # Convert the timestamp column to a datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Get unique dates in the DataFrame
    unique_dates = df['timestamp'].dt.date.unique()
    date = unique_dates[-1] 
    user_date = date.strftime('%Y-%m-%d')
    # print(user_date)
    
    # data processing
    filtered_df = df[df['timestamp'].dt.date == pd.to_datetime(user_date).date()]
    lastEntry = filtered_df.iloc[-1][0]
    filtered_df['hour'] = filtered_df['timestamp'].dt.hour
    hourly_running_time = filtered_df.groupby('hour')['timestamp'].count()

    # Convert the count to minutes
    hourly_running_time = hourly_running_time.where(hourly_running_time <= 60, 60)
    # print(hourly_running_time.sum()," Mins")
    return hourly_running_time.sum(),lastEntry, hourly_running_time.index, hourly_running_time.values
    

if __name__ == "__main__":
    imageGenerator()
