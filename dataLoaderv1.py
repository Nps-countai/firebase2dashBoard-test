import pyrebase
import time
from datetime import datetime,timedelta
import pandas as pd






def parse_datetime(datetime_str):
    try:
        
        current_datetime =  datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
        current_date = current_datetime.date()
        dayback = current_date + timedelta(days=1)
        startDay = current_date.strftime("%Y-%m-%d %H:%M:%S")
        endday = dayback.strftime("%Y-%m-%d %H:%M:%S")
        return startDay, endday
    except ValueError:
        try:
                current_datetime =  datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                current_date = current_datetime.date()
                dayback = current_date + timedelta(days=1)
                startDay = current_date.strftime("%Y-%m-%d %H:%M:%S")
                endday = dayback.strftime("%Y-%m-%d %H:%M:%S")
                return startDay, endday
        except:
                # only Date
                print('data not in proper format')




# tip process
def tip_data(i):
        try:
                wildcard_query = db.child(i).child("tip").order_by_child("timestamp").limit_to_last(1).get()
                od = wildcard_query.val()
                lsatDay = od[list(od.keys())[0]]['timestamp']
                # print('lsatDay : ',lsatDay)
                startDay, endday = parse_datetime(lsatDay)
                # print('start date:',startDay)
                # print('end date:',endday)
                
                datefilter_tip = db.child(i).child("tip").order_by_child("timestamp").start_at(startDay).end_at(endday).get()

                # print(len(datefilter_tip.val()))
                fbData = datefilter_tip.val()
                # print(fbData)
                # cone tip
                try:
                        temp_conetip = pd.json_normalize(fbData.values())
                except:
                        temp_conetip = pd.json_normalize(fbData)
                temp_conetip['millName'] = i
                temp_conetip['detectedcone'] = temp_conetip.apply(lambda x : True if (str(x['detectedconetype']) != str(x['selectedconetype'])) else False, axis=1) #detectedconetype
                # print(temp_conetip)
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
                # print('lsatDay : ',lsatDay)
                startDay, endday = parse_datetime(lsatDay)
                # print('start date:',startDay)
                # print('end date:',endday)
                
                datefilter_tip = db.child(i).child("uv").order_by_child("timestamp").start_at(startDay).end_at(endday).get()

                # print(len(datefilter_tip.val()))
                fbData = datefilter_tip.val()
                
                # cone tip
                try:
                        temp = pd.json_normalize(fbData.values())
                except:
                        temp = pd.json_normalize(fbData)
                temp['millName'] = i
                # print(temp)
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
                print('tip : ',od)
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
                print('uv: ',od)
                
                status = od[list(od.keys())[0]]['alarmstatus']
                fromtime = od[list(od.keys())[0]]['time']
                
                return status, fromtime
        except:
                print('uvalaram_data NONE')
                return 0, 0
      


firebaseConfig = {
        "apiKey": "AIzaSyANRoZgrkpyVG947sZYJVUFPfxEz3Z1mVc",
        "authDomain": "cone-inspection.firebaseapp.com",
        "databaseURL": "https://cone-inspection-default-rtdb.firebaseio.com",
        "projectId": "cone-inspection",
        "storageBucket": "cone-inspection.appspot.com",
        "messagingSenderId": "596245764155",
        "appId": "1:596245764155:web:1f0b0cfb91816b3cdb241e",
        "measurementId": "G-VQ7R8FJJSV"
        }
# db initial
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
# data define
uv_df = pd.DataFrame(columns=[])
conetip_df = pd.DataFrame(columns=[])
mill_list = []
final_df = pd.DataFrame(columns=['millName','conetip_Nondefect','conetip_Defect','conetip_total', 'defectPercen_CT','last_ctAt','uv_Nondefect','uv_Defect','uv_total', 'defectPercen_UV','last_uvAt' ,'lastactive','tip_Alrmstatus', 'tipstatus_fromtime','uv_Alrmstatus', 'uvstatus_fromtime'])

def updatedData():
        all_keys = db.child('/').shallow().get()
        n=0
        for i in all_keys.val():
                try:
                        n+=1
                        print(n)
                        mill_list.append(i)
                        conetip_Nondefect,conetip_Defect, defectPercen_CT,last_ctAt = tip_data(i)               
                        uv_Nondefect,uv_Defect, defectPercen_UV,last_uvAt = uv_data(i)               
                        tip_Alrmstatus, tipstatus_fromtime = tipalaram_data(i)
                        uv_Alrmstatus, uvstatus_fromtime = uvalaram_data(i)
                        print(uv_Alrmstatus, uvstatus_fromtime)
                        print(tip_Alrmstatus, tipstatus_fromtime)
                        
                        # final df
                        lastactive = last_uvAt if last_ctAt<last_uvAt else last_ctAt
                        data = [i,conetip_Nondefect,conetip_Defect,(conetip_Nondefect + conetip_Defect), defectPercen_CT,last_ctAt,uv_Nondefect,uv_Defect,(uv_Nondefect + uv_Defect), defectPercen_UV,last_uvAt,lastactive,tip_Alrmstatus, tipstatus_fromtime, uv_Alrmstatus, uvstatus_fromtime]
                        print(data)
                        final_df.loc[len(final_df)] = data
                        
                        
                        
                        print('name: ',i)
                        print('-------------------------------------------------------------------------------------------\n\n\n\n\n')
                except :
                        print()
                        print('failed  :',i)
                        print('-------------------------------------------------------------------------------------------\n\n\n\n\n')
                        
                
                        

                
        final_df.to_csv('finalDF.csv')
        return final_df



updatedData()
        