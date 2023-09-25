import json
import pandas as pd
import firebase_admin
from firebase_admin import db, credentials
import json
from datetime import datetime
from pandas import json_normalize






def updatedData():
    
    cred = credentials.Certificate("pg2fbtesting.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://cone-inspection-default-rtdb.firebaseio.com/"
        })

    ref = db.reference("/")
    fbData = ref.get()
    uv_df = pd.DataFrame(columns=[])
    conetip_df = pd.DataFrame(columns=[])
    mill_list = []
    final_df = pd.DataFrame(columns=['millName', 'totalCount','totaluvCount' ,'totalconetipCount' ,'total_uv_Defect', 'total_uv_Nondefect', 'total_conetip_Nondefect', 'total_conetip_Defect', 'lastDay_uv_Defect', 'lastDay_uv_Nondefect', 'lastDay_conetip_Nondefect', 'lastDay_conetip_Defect', 'lastuv_inspectionOn', 'lastconetip_inspectionOn','firstInspectionOn', 'lastDay_totaluvCount', 'lastDay_totalconetipCount', 'lastDay_totalCount','ldefectPercen_UV', 'ldefectPercen_CT', 'tdefectPercen_UV', 'tdefectPercen_CT'])

    for i in fbData:
        if i in ['bangladesh', 'indorama-turkey', 'lagnam','rswm', 'sagar','sitaramam']:
            print('millname: , ',i)
    
            mill_list.append(i)
            try:
                temp_conetip = pd.json_normalize(fbData[i]["tip"].values())
            except:
                temp_conetip = pd.json_normalize(fbData[i]["tip"])
            temp_conetip['millName'] = i
            
            try:
                temp_uv = pd.json_normalize(fbData[i]["uv"].values())
            except:
                temp_uv = pd.json_normalize(fbData[i]["uv"])
            temp_uv['millName'] = i  
            # print(temp_uv)
            temp_uv.to_csv('temp_uv.csv')
            uv_df =uv_df._append(temp_uv)
            temp_conetip['detectedcone'] = temp_conetip.apply(lambda x : True if (str(x['detectedconetype']) != str(x['selectedconetype'])) else False, axis=1) #detectedconetype
            conetip_df =conetip_df._append(temp_conetip)
            # print(temp_conetip)      
            temp_conetip.to_csv('temp_conetip.csv')
            
            
            
            
            
            # final df
            millName = i
            total_uv_Defect = (len(temp_uv[(temp_uv['detecteduv'] == 'True') ]))
            total_uv_Nondefect = (len(temp_uv[(temp_uv['detecteduv'] == 'False') ]))
            total_conetip_Nondefect = len(temp_conetip[(temp_conetip['detectedcone'] == False) ])
            total_conetip_Defect = len(temp_conetip[(temp_conetip['detectedcone'] == True) ])
            temp_conetip['timestamp'] = temp_conetip['timestamp'].astype(str)
            temp_uv['timestamp'] = temp_uv['timestamp'].astype(str)
            lastDay_uv_Defect = len(temp_uv[(temp_uv['detecteduv'] == True) & (temp_uv['timestamp'] == max(temp_uv['timestamp']))])
            lastDay_uv_Defect = len(temp_uv[(temp_uv['detecteduv'] == True) & (temp_uv['timestamp'] == max(temp_uv['timestamp']))])
            lastDay_uv_Nondefect = len(temp_uv[(temp_uv['detecteduv'] == 'False') & (temp_uv['timestamp'] == max(temp_uv['timestamp']))])
            # temp_conetip['detectedcone'].apply(lambda x: print(type(x)) if isinstance(x, str) else print(type(x)))
            
            print('working')
            lastDay_conetip_Nondefect = len(temp_conetip[(temp_conetip['detectedcone'] == False) & (temp_conetip['timestamp'] == max(temp_conetip['timestamp']))])
            print('lastDay_conetip_Nondefect done')
            lastDay_conetip_Defect = len(temp_conetip[(temp_conetip['detectedcone'] == True) & (temp_conetip['timestamp'] == max(temp_conetip['timestamp']))])
            print('lastDay_conetip_Defect done')
            lastuv_inspectionOn = max(temp_uv['timestamp'])
            print('lastuv_inspectionOn done')
            lastconetip_inspectionOn = max(temp_conetip['timestamp'])
            print('lastconetip_inspectionOn done')
            firstInspectionOn = min(temp_uv['timestamp']) if min(temp_uv['timestamp']) <= min(temp_conetip['timestamp']) else min(temp_conetip['timestamp'])    
            totalCount = total_uv_Defect + total_uv_Nondefect + total_conetip_Nondefect + total_conetip_Defect
            totaluvCount = total_uv_Defect + total_uv_Nondefect 
            totalconetipCount = total_conetip_Nondefect + total_conetip_Defect
            lastDay_totaluvCount = lastDay_uv_Defect + lastDay_uv_Nondefect
            lastDay_totalconetipCount = lastDay_conetip_Nondefect + lastDay_conetip_Defect
            lastDay_totalCount = lastDay_totaluvCount + lastDay_totalconetipCount 
            try:
                ldefectPercen_UV = (lastDay_uv_Defect / lastDay_totaluvCount) *100
            except ZeroDivisionError:
                ldefectPercen_UV = 0
            try:
                ldefectPercen_CT =  (lastDay_conetip_Defect / lastDay_totalconetipCount) * 100
            except ZeroDivisionError:
                ldefectPercen_CT = 0
            try:
                tdefectPercen_UV = (total_uv_Defect / totaluvCount) *100
            except ZeroDivisionError:
                tdefectPercen_UV = 0
            try:
                tdefectPercen_CT = (total_conetip_Defect / totalconetipCount) *100
            except ZeroDivisionError:
                tdefectPercen_CT = 0
            
            data = [millName, totalCount,totaluvCount ,totalconetipCount , total_uv_Defect, total_uv_Nondefect, total_conetip_Nondefect, total_conetip_Defect, lastDay_uv_Defect, lastDay_uv_Nondefect, lastDay_conetip_Nondefect, lastDay_conetip_Defect, lastuv_inspectionOn, lastconetip_inspectionOn,firstInspectionOn, lastDay_totaluvCount, lastDay_totalconetipCount, lastDay_totalCount,ldefectPercen_UV, ldefectPercen_CT, tdefectPercen_UV, tdefectPercen_CT]
            print('FP-uv  : ',ldefectPercen_UV,'Fp-CT : ',ldefectPercen_CT,"%" )
            final_df.loc[len(final_df)] = data
            print('fnal dne')
        
        


    print(final_df.head())
    final_df.to_csv('new.csv')
    return final_df


updatedData()
