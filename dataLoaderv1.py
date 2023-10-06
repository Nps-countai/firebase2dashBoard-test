import pyrebase
import time
from datetime import datetime,timedelta
import pandas as pd
import pytz



def parse_datetime(datetime_str):
    try:
        # with ms
        current_datetime =  datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S%z')
        current_date = current_datetime.date()
        dayback = current_date + timedelta(days=1)
        startDay = current_date.strftime("%Y-%m-%d %H:%M:%S")
        endday = dayback.strftime("%Y-%m-%d %H:%M:%S")
        return startDay, endday
        
        
    except ValueError:
        try:
                # without ms
                current_datetime =  datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f%z')
                current_date = current_datetime.date()
                dayback = current_date + timedelta(days=1)
                startDay = current_date.strftime("%Y-%m-%d %H:%M:%S")
                endday = dayback.strftime("%Y-%m-%d %H:%M:%S")
                return startDay, endday
            
        except ValueError:
                try:
                    # with ms
                    current_datetime =  datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                    current_date = current_datetime.date()
                    dayback = current_date + timedelta(days=1)
                    startDay = current_date.strftime("%Y-%m-%d %H:%M:%S")
                    endday = dayback.strftime("%Y-%m-%d %H:%M:%S")
                    return startDay, endday
                        
                except ValueError:
                        try:
                            # without ms
                            current_datetime =  datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                            current_date = current_datetime.date()
                            dayback = current_date + timedelta(days=1)
                            startDay = current_date.strftime("%Y-%m-%d %H:%M:%S")
                            endday = dayback.strftime("%Y-%m-%d %H:%M:%S")
                            return startDay, endday
                        except:
                            # only Date
                            print('data not in proper format')



def timezonenormalizer(datestr):
        if isinstance(datestr, str):
                try:
                        # Parse the timestamp and convert to UTC
                        timestamp = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S.%f%z')
                        utc_timestamp = timestamp.astimezone(pytz.UTC)
                        # Convert to Indian Standard Time (IST)
                        indian_timezone = pytz.timezone('Asia/Kolkata')
                        ist_timestamp = utc_timestamp.astimezone(indian_timezone)
                        # Format as a string
                        formatted_timestamp = ist_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f%z')
                        return formatted_timestamp
                except ValueError:
                        # Parse the timestamp and convert to UTC
                        timestamp = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S%z')
                        utc_timestamp = timestamp.astimezone(pytz.UTC)
                        # Convert to Indian Standard Time (IST)
                        indian_timezone = pytz.timezone('Asia/Kolkata')
                        ist_timestamp = utc_timestamp.astimezone(indian_timezone)
                        # Format as a string
                        formatted_timestamp = ist_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f%z')
                        return formatted_timestamp
        else:
                print('int type')


# tip process
def tip_data(i):
        try:
                wildcard_query = db.child(i).child("tip").order_by_child("timestamp").limit_to_last(1).get()
                od = wildcard_query.val()
                lsatDay = od[list(od.keys())[0]]['timestamp']
                startDay, endday = parse_datetime(lsatDay)
                datefilter_tip = db.child(i).child("tip").order_by_child("timestamp").start_at(startDay).end_at(endday).get()
                fbData = datefilter_tip.val()
                               
                # cone tip
                try:
                        temp_conetip = pd.json_normalize(fbData.values())
                except:
                        temp_conetip = pd.json_normalize(fbData)
                        
                temp_conetip['millName'] = i
                temp_conetip['detectedcone'] = temp_conetip.apply(lambda x : True if (str(x['detectedconetype']) != str(x['selectedconetype'])) else False, axis=1) #detectedconetype
                
                #conetip
                conetip_Nondefect = len(temp_conetip[(temp_conetip['detectedcone'] == False) ])
                conetip_Defect = len(temp_conetip[(temp_conetip['detectedcone'] == True) ])
                total_tip = conetip_Nondefect + conetip_Defect
                
                try:
                        defectPercen_CT =  (conetip_Defect / total_tip) * 100
                except ZeroDivisionError:
                        defectPercen_CT = 0                
                return conetip_Nondefect,conetip_Defect, defectPercen_CT, lsatDay
        except:                
                print('tipdata NONE')
                return 0, 0, 0,lsatDay
                

# uv process
def uv_data(i):
        try: 
                wildcard_query = db.child(i).child("uv").order_by_child("timestamp").limit_to_last(1).get()
                od = wildcard_query.val()
                lsatDay = od[list(od.keys())[0]]['timestamp']
                startDay, endday = parse_datetime(lsatDay)
                datefilter_tip = db.child(i).child("uv").order_by_child("timestamp").start_at(startDay).end_at(endday).get()
                fbData = datefilter_tip.val()
                
                # cone tip
                try:
                        temp = pd.json_normalize(fbData.values())
                except:
                        temp = pd.json_normalize(fbData)
                temp['millName'] = i
                
                #uv        
                uv_Nondefect = len(temp[(temp['detecteduv'] == 'False') ])
                uv_Defect = len(temp[(temp['detecteduv'] == 'True') ])
                total_uv = uv_Nondefect + uv_Defect              
                             
                try:
                        ldefectPercen_UV = (uv_Defect / total_uv) *100
                except ZeroDivisionError:
                        ldefectPercen_UV = 0
                return uv_Nondefect,uv_Defect, ldefectPercen_UV, lsatDay
        except:
                print('uvdata NONE')
                return 0, 0, 0,lsatDay

# tipalaram
def tipalaram_data(i):
        try: 
                wildcard_query = db.child(i).child("tipalarm").order_by_child("start_time").limit_to_last(1).get()
                od = wildcard_query.val()
                status = od[list(od.keys())[0]]['alarm_status']
                fromtime = od[list(od.keys())[0]]['start_time']                
                return status, fromtime
        except:
                print('tipalaram_data NONE')
                return 0, 0
        

# tipalaram
def uvalaram_data(i):
        try: 
                wild_query = db.child(i).child("uvalarm").order_by_child("time").limit_to_last(1).get()
                od = wild_query.val()
                status = od[list(od.keys())[0]]['alarmstatus']
                fromtime = od[list(od.keys())[0]]['time']
                
                return status, fromtime
        except:
                print('uvalaram_data NONE')
                return 0, 0
      


firebaseConfig = {
        "apiKey": "AIzaSyBxn5dlUSpeogE8iT8ZdcC07LSr0Dxtk78",
        "authDomain": "conei-4a476.firebaseapp.com",
        "databaseURL": "https://conei-4a476-default-rtdb.firebaseio.com",
        "projectId": "conei-4a476",
        "storageBucket": "conei-4a476.appspot.com",
        "messagingSenderId": "99303364339",
        "appId": "1:99303364339:web:2b35fa36a438119edd4986",
        "measurementId": "G-QT2CRBY4NX"
        }

# db initial
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# data define
uv_df = pd.DataFrame(columns=[])
conetip_df = pd.DataFrame(columns=[])

def updatedData():
        while True:
                mill_list = []
                final_df = pd.DataFrame(columns=['millName','conetip_Nondefect','conetip_Defect','conetip_total', 'defectPercen_CT','last_ctAt','uv_Nondefect','uv_Defect','uv_total', 'defectPercen_UV','last_uvAt' ,'lastactive','tip_Alrmstatus', 'tipstatus_fromtime','uv_Alrmstatus', 'uvstatus_fromtime'])

                all_keys = db.child('/').shallow().get()
                n=0
                for i in all_keys.val():
                        try:
                                n+=1
                                print('millNO : ',n)
                                mill_list.append(i)
                                conetip_Nondefect,conetip_Defect, defectPercen_CT,last_ctAt = tip_data(i)               
                                uv_Nondefect,uv_Defect, defectPercen_UV,last_uvAt = uv_data(i)               
                                tip_Alrmstatus, tipstatus_fromtime = tipalaram_data(i)
                                uv_Alrmstatus, uvstatus_fromtime = uvalaram_data(i)
                                
                                last_ctAt = timezonenormalizer(last_ctAt)
                                last_uvAt = timezonenormalizer(last_uvAt) 
                                tipstatus_fromtime = timezonenormalizer(tipstatus_fromtime) 
                                uvstatus_fromtime = timezonenormalizer(uvstatus_fromtime) 
                                # final df
                                lastactive = last_uvAt if last_ctAt<last_uvAt else last_ctAt
                                # print(last_ctAt)
                                data = [i,conetip_Nondefect,conetip_Defect,(conetip_Nondefect + conetip_Defect), defectPercen_CT,last_ctAt,uv_Nondefect,uv_Defect,(uv_Nondefect + uv_Defect), defectPercen_UV,last_uvAt,lastactive,tip_Alrmstatus, tipstatus_fromtime, uv_Alrmstatus, str(uvstatus_fromtime)]
                                # print(data)
                                final_df.loc[len(final_df)] = data                               
                                                                
                                print('name: ',i)
                                print('-------------------------------------------------------------------------------------------\n')
                        except :
                                print()
                                print('failed  :',i)
                                print('-------------------------------------------------------------------------------------------\n')
                
                final_df.to_csv('finalDF.csv')
                print('Last sync on : ',datetime.now())
                print("Syncing......")
                time.sleep(30)
                


updatedData()
        