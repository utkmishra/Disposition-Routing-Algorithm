#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thrus Jan 20 2022

@author: Utkarsh Mishra
"""



#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np, pandas as pd
from datetime import timedelta
import math
from datetime import datetime


## In[2]:

bom= pd.read_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/ATTBOM Jan 3rd, 2022.xlsx")

onhand= pd.read_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/ATTOnHand Jan 3rd, 2022.xlsx")

## Remove duplicate records from Demand file then consume
demand = pd.read_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/ATT Lab DSA Jan 3rd, 2022.xlsx") 

model_list = pd.read_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/Model List Nov 23rd, 2021.xlsx")

keep_list = pd.read_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/EO Q4-21 keep quantities.xlsx")





#bom= pd.read_excel(r"/home/shubhamrelekar/Desktop/On Hand & BOM Sep 30th, 2021.xlsx", sheet_name='tblBillOfMaterial', engine='openpyxl')

#onhand= pd.read_excel(r"/home/shubhamrelekar/Desktop/On Hand & BOM Sep 30th, 2021.xlsx", sheet_name="tblOnHandInventory ", engine='openpyxl')

#demand = pd.read_excel(r"/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/allexcel_files/ATT Lab DSA Sep 30th, 2021.xlsx", engine='openpyxl')

#model_list = pd.read_excel(r"/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/Input Files/Model List Nov 23rd, 2021.xlsx", sheet_name="By Part", engine='openpyxl')

#keep_list = pd.read_excel(r"/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/Input Files/EO Q4-21 keep quantities.xlsx", engine='openpyxl')


# In[3]:


demand["Demand_Future_12_Month"] = demand["ShortageReportSubsetDemand"]+demand["AccruedDemand"]+demand["ASCPDemand"]+demand["Demand1"]+demand["Demand2"]+demand["Demand3"]+demand["Demand4"]+demand["Demand5"]+demand["Demand6"]+demand["SeventhMonthAndBeyondDemand"]
ms=onhand.copy()

#ms=ms[(ms["ATTItemNumber"]!="TBUY")&(ms["ATTItemNumber"].notnull())&(ms["WWTPartClassification"]!="Integrated Component")&(ms["Contract"].isin(["EPL","GCRMA"]))]
ms_integrated = ms[ms["WWTPartClassification"] == "Integrated Component"]
ms=ms[(ms["ATTItemNumber"]!="TBUY")&(ms["ATTItemNumber"].notnull())&(ms["WWTPartClassification"]!="Integrated Component")]

#ms["Is_Parent"] = np.where(((ms['ItemType']=='Standard')&(ms['TbuyOnlyParent'] == 'N')), 'comp',
#                           np.where(((ms['ItemType']=='PTO KIT')|(ms['TbuyOnlyParent'] == 'Y')),'par','N-A'))

ms["Is_Parent"] = np.where(ms['ATTItemNumber'].isin(bom['ParentATTItem']),'par',np.where(ms['ATTItemNumber'].isin(bom['ComponentATTItem']),'comp','N-A'))
    

ms['dateOfReport']= pd.to_datetime(ms['dateOfReport']) 
ms['OrigDateReceived']= pd.to_datetime(ms['OrigDateReceived'])
ms['Aging'] = (ms['dateOfReport'] - ms['OrigDateReceived'])/timedelta(days=365)
print(ms.shape, np.sum(ms['QuantityOnhand']))

disposition_mapping = pd.DataFrame({'MaterialDesignator': {0: 'ATT/LAB - C',
                                                           1: 'ATT/PRJCT - C',
                                                           2: 'ATTWIC/LAB - C',
    3: 'ATT/INTRL - C',
    4: 'ATT/NOK - C',
    5: 'ATT/RAW - C',
    6: 'ATT/REPRET - C',
    7: 'ATT/STOCK - C',
    8: 'ATT-DNSTL - C',
    9: 'ATTKSTOCK - C',
    10: 'ATT-NCMPT - C',
    11: 'ATTPCN - C',
    12: 'ATT - C',
    13: 'ATT/QUAR - C',
    14: 'ATTAP - C',
    15: 'ATT-K - C',
    16: 'ATTNOPICK - C',
    17: 'ATTNOPICK-K - C',
    18: 'ATTWIC - C',
    19: 'ATTWIC/QUAR - C',
    20: 'ATTWIC-K - C',
    21: 'GCRMA/INTRL - C',
    22: 'GCRMA/QUAR - C',
    23: 'GCRMA/STOCK - C',
    24: 'GCRMA-DNSTL - C',
    25: 'GCRMAKSTOCK - C',
    26: 'GCRMAPCN - C',
    27: 'GCRMAOEM - C',
    28: 'GCRMAOEM-K - C',
    29: 'ATTAP/K - C'},
    'DISPOSITION': {0: 'LAB',
    1: 'LAB',
    2: 'LAB',
    3: 'ATT/INTRL - C',
    4: 'ATT/NOK - C',
    5: 'Not Decided',
    6: 'ATT/REPRET - C',
    7: 'Not Decided',
    8: 'Not Decided',
    9: 'Not Decided',
    10: 'ATT-NCMPT - C',
    11: 'ATTPCN - C',
    12: 'READY TO DEPLOY',
    13: 'ATT/QUAR - C',
    14: 'Not Decided',
    15: 'READY TO DEPLOY',
    16: 'ATTNOPICK - C',
    17: 'ATTNOPICK-K - C',
    18: 'ATTWIC - C',
    19: 'ATTWIC/QUAR - C',
    20: 'ATTWIC-K - C',
    21: 'GCRMA/INTRL - C',
    22: 'GCRMA/QUAR - C',
    23: 'Not Decided',
    24: 'Not Decided',
    25: 'Not Decided',
    26: 'GCRMAPCN - C',
    27: 'Not Decided',
    28: 'Not Decided',
    29: 'Not Decided'}})
ms = ms.merge(disposition_mapping, on='MaterialDesignator', how='left')

MD_Pri = pd.DataFrame({'MaterialDesignator': ['ATT - C','ATT-K - C','ATT/LAB - C','ATT/PRJCT - C','ATTWIC/LAB - C','ATTAP - C','ATTAP/K- C','ATT/STOCK - C',
                                         'ATTKSTOCK - C','ATT-DNSTL - C','ATT/RAW - C','GCRMAOEM - C',
                                         'GCRMAOEM-K - C','GCRMA/STOCK - C' , 'GCRMAKSTOCK - C','GCRMA-DNSTL - C'],
                 'MD_Priority': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]})

#ms.loc[ms['DISPOSITION'] == 'N-A', 'DISPOSITION'] = ms.loc[ms['MaterialDesignator']]

ms = ms.merge(model_list[["CEQ","Shopping List MODEL"]],left_on="ATTItemNumber",right_on="CEQ",how="left").rename(columns={"Shopping List MODEL":"Model"}).drop("CEQ",axis = 1).fillna("N-A")
#ms.to_excel('/home/shubhamrelekar/Desktop/ms.xlsx')

# In[4]:   
ms_integrated["Is_Parent"] = 'comp'
ms_integrated['dateOfReport']= pd.to_datetime(ms_integrated['dateOfReport']) 
ms_integrated['OrigDateReceived']= pd.to_datetime(ms_integrated['OrigDateReceived'])
ms_integrated['Aging'] = (ms_integrated['dateOfReport'] - ms_integrated['OrigDateReceived'])/timedelta(days=365)
ms_integrated = ms_integrated.merge(disposition_mapping, on='MaterialDesignator', how='left')
ms_integrated = ms_integrated.merge(model_list[["CEQ","Shopping List MODEL"]],left_on="ATTItemNumber",right_on="CEQ",how="left").rename(columns={"Shopping List MODEL":"Model"}).drop("CEQ",axis = 1).fillna("N-A")

#ms_integrated = ms_integrated.merge(model_list[["CEQ","Shopping List MODEL"]],left_on="ATTItemNumber",right_on="CEQ",how="left").rename(columns={"Shopping List MODEL":"Model"}).drop("CEQ",axis = 1).fillna("N-A")
    

# In[5]:

Final_Df = pd.DataFrame()


# In[6]:
#ms=ms[ms['Model'] == 'UMTS Cabinet Core Ericsson 3308 Micro']
#ms=ms[ms['Model']=='CEQ31706 / CEQ28224 / CEQ13381']
#ms=ms[ms['Model']=='CEQ11664 / CEQ44808 / CEQ49088']
#ms=ms[ms['Model'].isin(['CEQ44615 / CEQ44616 / CEQ44619 / CEQ44767 / CEQ45792 / CEQ47784'])]
#ms=ms[ms['Model'].isin(['CEQ11612 / CEQ10466','ANT10070 / ANT13335'])]
#ms=ms[ms['ATTItemNumber'].isin(['CEQ.10566','NEQ.15452','CEQ.11989'])]
#ms_integrated=ms_integrated[ms_integrated['ATTItemNumber'].isin(['CEQ.10487','CEQ.10489','CEQ.11818','CEQ.26213'])]
#ms=ms[ms['ATTItemNumber']=='NEQ.19873']
#ms=ms[ms['ATTItemNumber']=='SEQ.28595']
#ms=ms[ms['Model']=='SEQ11921 / SEQ16249']
#ms=ms[ms['ATTItemNumber']=='CEQ.52796']
#ms=ms[ms['Model']=='CEQ11664 / CEQ44808 / CEQ49088']
#ms=ms[ms['Model']=='NEQ00794']
#ms=ms[ms['Model']=='NEQ00704']
#ms=ms[ms['Model']=='CEQ10123']
#ms=ms[ms['Model']=='NEQ15637']#***
#ms=ms[ms['Model']=='NEQ15852 / NEQ12410 / NEQ01032']#***
#ms=ms[ms['Model']=='CEQ10549 / CEQ31909 / CEQ14177 / CEQ14400 / CEQ17568']
#ms=ms[ms['Model']=='ANT46062 / ANT44730 / ANT15363 / ANT15101']
#ms=ms[ms['Model'].isin(['NEQ01481','TE20 Outdoor 48V Power Cabinet','NEQ15852 / NEQ12410 / NEQ01032'])]
#ms=ms[ms['Model'].isin(['CEQ18593 / CEQ47449 / CEQ18091','CEQ18502 / CEQ20142 / CEQ45942 / CEQ47056','CEQ18500 / CEQ20198 / CEQ21288 / CEQ45762','CEQ18088','CEQ18594','CEQ18654','CEQ47451'])]
#ms.to_excel('/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/allexcel_files/MutiModelEx.xlsx')
#ms=ms[ms['Model']=='CEQ18500 / CEQ20198 / CEQ21288 / CEQ45762']


# In[5]:


all_Item = list(set(ms['ATTItemNumber']))  
all_Model = list(set(ms["Model"])) 


# # Data Preparation for Substitution

# In[6]:


print("Data Preparation for Substitution | Start Time-{}".format(datetime.now()))

demand_item_past_12 = list()
demand_item_future_12 = list()
demand_model_past_12 = list()
demand_model_future_12 = list()
Model_Onhand_Total_Available = []
Model_Onhand_EPL_Available = []
Model_Onhand_GCRMA_Available = []
Item_Onhand_Total_Available = []
Item_Onhand_EPL_Available = []
Item_Onhand_GCRMA_Available = []
mixed_model = []

for i in all_Item:
    temp_item = demand[demand["ATTItemNumber"]==i]
    temp_item_oh=ms[ms['ATTItemNumber']==i]
    
    try:
        dem_p = int(temp_item["TwelveMonthShippingTotal"])
        demand_item_past_12.append(dem_p)
    except:
        demand_item_past_12.append(0)
    try:
        dem_f = int(temp_item["Demand_Future_12_Month"])
        demand_item_future_12.append(dem_f)
    except:
        demand_item_future_12.append(0)
    try:
        epl_oh_avlbl = temp_item_oh[(temp_item_oh["DISPOSITION"].isin(["LAB","READY TO DEPLOY","Not Decided"])) & (temp_item_oh["Contract"] == "EPL")]
        epl_avlbl = int(np.sum(epl_oh_avlbl["QuantityOnhand"]))
        Item_Onhand_EPL_Available.append(epl_avlbl)
    except:
        Item_Onhand_EPL_Available.append(0)
    try:
        gcrma_oh_avlbl = temp_item_oh[(temp_item_oh["DISPOSITION"].isin(["READY TO DEPLOY","LAB","Not Decided"])) & (temp_item_oh["Contract"] == "GCRMA")]
        gcrma_avlbl = int(np.sum(gcrma_oh_avlbl["QuantityOnhand"]))
        Item_Onhand_GCRMA_Available.append(gcrma_avlbl)
    except:
        Item_Onhand_GCRMA_Available.append(0)

item_info = pd.DataFrame({"ATTItemNumber":all_Item,"Demand_Past_12_Month":demand_item_past_12,
                          "Demand_Future_12_Month":demand_item_future_12,"Item EPL Available Qty":Item_Onhand_EPL_Available,
                          "Item GCRMA Available Qty":Item_Onhand_GCRMA_Available})

ms=ms.merge(item_info,on="ATTItemNumber",how='left')

for j in all_Model:
    unique_is_par = []
    if j == "N-A":
        demand_model_past_12.append(0)
        demand_model_future_12.append(0)
        Model_Onhand_EPL_Available.append(0)
        Model_Onhand_GCRMA_Available.append(0)
        continue
    
    temp_model=ms[ms["Model"]==j]
    unique_is_par=temp_model.Is_Parent.unique()
    
    par_chk = all(x in unique_is_par for x in ['comp', 'par'])
    
    if not par_chk:
        pivot=pd.pivot_table(temp_model,values=['Item EPL Available Qty','Demand_Future_12_Month','Demand_Past_12_Month','Item GCRMA Available Qty'],index=['ATTItemNumber'],aggfunc=np.mean)
        try:
            dem_m_p=int(np.sum(pivot["Demand_Past_12_Month"]))
            demand_model_past_12.append(dem_m_p)
        except:
            demand_model_past_12.append(0)
        try:
            dem_m_f=int(np.sum(pivot["Demand_Future_12_Month"]))
            demand_model_future_12.append(dem_m_f)
        except:
            demand_model_future_12.append(0)
        try:
            m_epl=int(np.sum(pivot["Item EPL Available Qty"]))
            Model_Onhand_EPL_Available.append(m_epl)
        except:
            Model_Onhand_EPL_Available.append(0)
        try:
            m_gcrma=int(np.sum(pivot["Item GCRMA Available Qty"]))
            Model_Onhand_GCRMA_Available.append(m_gcrma)
        except:
            Model_Onhand_GCRMA_Available.append(0)
    else:
        demand_model_past_12.append('-')
        demand_model_future_12.append('-')
        Model_Onhand_EPL_Available.append('-')
        Model_Onhand_GCRMA_Available.append('-')
        mixed_model.append(j) 
        
mixed_model_df=ms[ms['Model'].isin(mixed_model)]
#mixed_model_df.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/mixed_model_df.xlsx")
ms=ms[~ms['Model'].isin(mixed_model)]
        
model_info = pd.DataFrame({'Model':all_Model,'Model_Demand_Past_12_Month':demand_model_past_12,
                          'Model_Demand_Future_12_Month':demand_model_future_12,'Model EPL Available Qty':Model_Onhand_EPL_Available,
                          'Model GCRMA Available Qty':Model_Onhand_GCRMA_Available})   

ms=ms.merge(model_info,on='Model',how='left')

ms['Item Delta']=ms['Item EPL Available Qty']+ms['Item GCRMA Available Qty']-ms['Demand_Future_12_Month']
ms['Model Delta']=ms['Model EPL Available Qty']+ms['Model GCRMA Available Qty']-ms['Model_Demand_Future_12_Month']

ms=ms.merge(MD_Pri,on='MaterialDesignator',how='left')

DUS_lookup = demand[['ATTItemNumber','DaysUntilShortage']]
ms=ms.merge(DUS_lookup,on='ATTItemNumber',how='left') 
ms.DaysUntilShortage = ms.DaysUntilShortage.fillna('No Shortage') 
ms['Disposition_Final'] = 'x'
ms['Destination'] = 'y'

#ms_other_contract = ms[~ms['Contract'].isin(["EPL","GCRMA"])]
# Selecting items with Available Disposition
df2 = ms[ms['DISPOSITION'].isin(['Not Decided', 'READY TO DEPLOY', 'LAB'])]
#df2.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/df2.xlsx")
print("Data Preparation for Substitution | End Time-{}".format(datetime.now()))


# # Data Preparation for Substitution END

# In[7]:

integrated_items = list(ms_integrated.ATTItemNumber.unique())
integrated_model = list(set(ms_integrated["Model"]))

demand_integrated_item_past_12 = list()
demand_integrated_item_future_12 = list()
demand_integrated_model_past_12 = list()
demand_integrated_model_future_12 = list()

for e in integrated_items:
    temp_int_item = demand[demand["ATTItemNumber"]==e]
    
    try:
        int_dem_p = int(temp_int_item["TwelveMonthShippingTotal"])
        demand_integrated_item_past_12.append(int_dem_p)
    except:
        demand_integrated_item_past_12.append(0)
    try:
        int_dem_f = int(temp_int_item["Demand_Future_12_Month"])
        demand_integrated_item_future_12.append(int_dem_f)
    except:
        demand_integrated_item_future_12.append(0)

int_item_info = pd.DataFrame({"ATTItemNumber":integrated_items,"Demand_Past_12_Month":demand_integrated_item_past_12,
                          "Demand_Future_12_Month":demand_integrated_item_future_12})

ms_integrated=ms_integrated.merge(int_item_info,on="ATTItemNumber",how='left')
ms_integrated["Item EPL Available Qty"] = 0 
ms_integrated["Item GCRMA Available Qty"] = 0

for y in integrated_model:
    if y == "N-A":
        demand_integrated_model_past_12.append(0)
        demand_integrated_model_future_12.append(0)
        continue
    temp_int_model=ms_integrated[ms_integrated["Model"]==y] 
    pivot_int=pd.pivot_table(temp_int_model,values=['Demand_Future_12_Month','Demand_Past_12_Month'],index=['ATTItemNumber'],aggfunc=np.mean)
    try:
        dem_int_m_p=int(np.sum(pivot_int["Demand_Past_12_Month"]))
        demand_integrated_model_past_12.append(dem_int_m_p)
    except:
        demand_integrated_model_past_12.append(0)
    try:
        dem_int_m_f=int(np.sum(pivot_int["Demand_Future_12_Month"]))
        demand_integrated_model_future_12.append(dem_int_m_f)
    except:
        demand_integrated_model_future_12.append(0)
    
int_model_info = pd.DataFrame({'Model':integrated_model,'Model_Demand_Past_12_Month':demand_integrated_model_past_12,
                          'Model_Demand_Future_12_Month':demand_integrated_model_future_12})   

ms_integrated=ms_integrated.merge(int_model_info,on='Model',how='left')
ms_integrated["Model EPL Available Qty"] = 0
ms_integrated["Model GCRMA Available Qty"] = 0
ms_integrated["Item Delta"] = 0
ms_integrated["Model Delta"] = 0
ms_integrated = ms_integrated.merge(MD_Pri, on='MaterialDesignator', how='left')
ms_integrated=ms_integrated.merge(DUS_lookup,on='ATTItemNumber',how='left') 
ms_integrated.DaysUntilShortage = ms_integrated.DaysUntilShortage.fillna('No Shortage') 
ms_integrated['Disposition_Final'] = 'x'
ms_integrated['Destination'] = 'y'
ms_integrated["Qty Left After Substitution"] = 0
ms_integrated["Qty Required After Substitution"] = 0
   
ms_integrated['Model_Safety_Net'] = np.where(ms_integrated.Model == 'N-A',0,
                    np.where(ms_integrated.Model_Demand_Past_12_Month > ms_integrated.Model_Demand_Future_12_Month,
                             3*ms_integrated.Model_Demand_Past_12_Month, 3*ms_integrated.Model_Demand_Future_12_Month))

# In[8]:
try_model = list(df2.Model.unique())
uniq_items = list(df2.ATTItemNumber.unique())

# # Substitution Logic

# In[9]:


print("Substitution Logic | Start Time-{}".format(datetime.now()))
issue_mod = []
temp_df1 = pd.DataFrame()

non_inv_items_list = list(set(demand['ATTItemNumber']) - set(df2['ATTItemNumber']))

for j in try_model:
    
    if j == "N-A":
        model_na_df = df2[df2['Model'] == j]
        temp_df1 = temp_df1.append(model_na_df)
        continue
    
    try:
        model_df=df2[df2["Model"]==j]
        #mod_item=list(model_df.ATTItemNumber.unique())
        mod_item_df = model_list[model_list['Shopping List MODEL'] == j]
        mod_item = list(mod_item_df.CEQ.unique())
#        mod_item_cnt = len(mod_item)
        subBackend_stg1 = pd.pivot_table(model_df,index=['ATTItemNumber','DaysUntilShortage','MarketPrice'],
                                         values=['Demand_Future_12_Month','Item EPL Available Qty','Item GCRMA Available Qty'],
                                         aggfunc={'Demand_Future_12_Month':np.mean,'Item EPL Available Qty':np.mean,'Item GCRMA Available Qty':np.mean})       
        
        subBackend_stg1['tmp'] =  subBackend_stg1.index 
        subBackend_stg1[['ATTItemNumber', 'DaysUntilShortage', 'MarketPrice']] = pd.DataFrame(subBackend_stg1['tmp'].tolist(), index=subBackend_stg1.index)
        subBackend_stg1.drop('tmp', axis='columns', inplace=True)
        subBackend_stg1.index = range(0,len(subBackend_stg1['ATTItemNumber']))
        not_in_inv_list = list(set(mod_item) - set(subBackend_stg1['ATTItemNumber']))      
        
        filtered_df = demand[demand['ATTItemNumber'].isin(not_in_inv_list)][['Demand_Future_12_Month','ATTItemNumber','DaysUntilShortage','MarketPrice']]
        filtered_df['Item EPL Available Qty'] = 0
        filtered_df['Item GCRMA Available Qty'] = 0 
        filtered_df = filtered_df[["Demand_Future_12_Month", "Item EPL Available Qty", "Item GCRMA Available Qty" ,"ATTItemNumber", "DaysUntilShortage", "MarketPrice"]]
        
        subBackend_stg1 = subBackend_stg1.append(filtered_df)
        
        #subBackend_stg1 = subBackend_stg1.reset_index()
        subBackend_stg1['Item_delta'] = subBackend_stg1['Item EPL Available Qty'] + subBackend_stg1['Item GCRMA Available Qty'] - subBackend_stg1['Demand_Future_12_Month']
        subBackend_stg1['Sub_required'] = np.where(subBackend_stg1.Item_delta >= 0, 0, 1)
        subBackend_stg1['Sub_Supply'] = np.where(subBackend_stg1.Item_delta >= 0, 1, 0)
        subBackend_stg1['DaysUntilShortage'] = subBackend_stg1['DaysUntilShortage'].replace(['Critical Shortage'],0)
        subBackend_stg1['DaysUntilShortage'] = subBackend_stg1['DaysUntilShortage'].replace(['No Shortage'],99999)
        posDelta = subBackend_stg1[subBackend_stg1['Item_delta'] >= 0]
        negDelta = subBackend_stg1[subBackend_stg1['Item_delta'] < 0] 
    
        posDelta = posDelta.sort_values(['DaysUntilShortage', 'Item_delta'], ascending=[False, False])
        negDelta = negDelta.sort_values(['DaysUntilShortage', 'MarketPrice'], ascending=[True, False])
    
        newSubBackend_stg1 = pd.concat([negDelta, posDelta])
    
        newSubBackend_stg1['Fullfilment_Priority'] = list(range(1,len(subBackend_stg1)+1))
        newSubBackend_stg1.loc[newSubBackend_stg1.Sub_Supply == 1, 'Fullfilment_Priority'] = np.nan
        newSubBackend_stg1 = newSubBackend_stg1.sort_values('Fullfilment_Priority')
    
        FinalReq_dict = {}
        reqQty_dict = {}
        total_required = 0
        newSubBackend_stg1['From'] = '-'
        newSubBackend_stg1['To'] = '-'
        newSubBackend_stg1['Qty'] = '-'
        for i, r in newSubBackend_stg1.iterrows():
            to_list = []
            qty_list = []
            item = r['ATTItemNumber']
            if r['Sub_required'] == 1:
                reqQty_dict[item] = abs(r['Item_delta'])
                total_required = total_required + abs(r['Item_delta'])
    #                 print("{} | reqQty_dict: {}".format(i,reqQty_dict))
    #                 print("{} |total_required: {}".format(i,total_required))
            else:
                if r['Item_delta'] >0:
                    item_available = r['Item_delta']
                    #print("{} | item_available: {}".format(i,item_available))
                    for key, val in reqQty_dict.items():
    #                         print("key: {}".format(key))
    #                         print("val: {}".format(val))
                        if val >= item_available:
                            val = val - item_available
                            reqQty_dict[key] = val
                            qty_list.append(item_available)
                            to_list.append(key)
                        else:
                            item_available = item_available - val
                            reqQty_dict[key] = 0
                            qty_list.append(val)
                            to_list.append(key)
    
    #                             print("reqQty_dict: {}".format(reqQty_dict))
    #                             print("key: {}".format(key))
    #                             print("val: {}".format(val)) 
    #                             print("qty_list: {}".format(qty_list))
    #                             print("to_list: {}".format(to_list))
    
                newSubBackend_stg1.at[i, 'From'] = item
                newSubBackend_stg1.at[i, 'To'] = to_list
                newSubBackend_stg1.at[i, 'Qty'] = qty_list
    
            if newSubBackend_stg1.at[i,'From'] == '-':
                FinalReq_dict[r['ATTItemNumber']] = 0
            else:
                tpDict = {}
                for index, value in enumerate(to_list):
                    tpDict[value] = qty_list[index]
    
                FinalReq_dict[r['ATTItemNumber']] = tpDict
    
        #print(FinalReq_dict)
        mod_item_list = list(set(newSubBackend_stg1['ATTItemNumber']))
        for i in mod_item_list: 
            to_Give = FinalReq_dict[i]
            try:
                to_Give_qty = sum(to_Give.values())
            except:
                to_Give_qty = 0
            temp_df=model_df[model_df['ATTItemNumber'] == i]
            temp_df2 = pd.DataFrame()
            demand_left=np.mean(temp_df['Demand_Future_12_Month'])
            temp_df = temp_df.sort_values(['MD_Priority','Aging','QuantityOnhand'],ascending=[True,True,True])
            temp_df=temp_df.reset_index(drop=True)
    
            for k, row in temp_df.iterrows():
                try:
                    del(split1)
                    del(split2)
                    del(split3)
                except:
                    pass
    
                if (row['Disposition_Final'] == 'x') & (row['Destination'] == 'y'):
                        #print(to_Give_qty)
                        if (demand_left > 0):
                            if demand_left >= int(row['QuantityOnhand']):
                                demand_left = demand_left - int(row['QuantityOnhand'])
                                if row['DISPOSITION'] == 'READY TO DEPLOY':
                                    temp_df.at[k,'Disposition_Final'] = 'READY TO DEPLOY'
                                    temp_df.at[k,'Destination'] = row['ATTItemNumber']
                                else:
                                    temp_df.at[k,'Disposition_Final'] = 'LAB'
                                    temp_df.at[k,'Destination'] = row['ATTItemNumber']
                            else:
                                bal = int(row['QuantityOnhand']) - demand_left
                                split1 = dict(row)
                                split2 = dict(row)
                                split1['QuantityOnhand'] = demand_left
                                demand_left = 0
                                if row['DISPOSITION'] == 'READY TO DEPLOY':
                                    split1['Disposition_Final'] = 'READY TO DEPLOY'
    
                                else:
                                    split1['Disposition_Final'] = 'LAB'
    
                                split1['Destination'] = row['ATTItemNumber'] 
                                
                                if to_Give_qty == 0:
                                    split2['QuantityOnhand'] = bal
                                else:
                                    flag1 = 1
                                    for key, val in to_Give.items():
                                        if flag1 == 1:
                                            if val == 0: 
                                                pass
                                            else:
                                                if bal <= val:
                                                    split2['QuantityOnhand'] = bal 
                                                    if split2['DISPOSITION'] == 'READY TO DEPLOY':
                                                        split2['Disposition_Final'] = 'RTD_SUBSTITUTE'
                                                    else:
                                                        split2['Disposition_Final'] = 'LAB_SUBSTITUTE'
    
                                                    split2['Destination'] = key
                                                    to_Give_qty = to_Give_qty - bal
                                                    to_Give[key] = val-bal
                                                    flag1 = 0
                                                else:
                                                    bal = bal - val
                                                    split3 = dict(row)
    
                                                    split2['QuantityOnhand'] = val 
    
                                                    if split2['DISPOSITION'] == 'READY TO DEPLOY':
                                                        split2['Disposition_Final'] = 'RTD_SUBSTITUTE'
                                                    else:
                                                        split2['Disposition_Final'] = 'LAB_SUBSTITUTE'
    
                                                    to_Give_qty = to_Give_qty - val
                                                    split2['Destination'] = key
                                                    to_Give[key] = 0
    
                                                    split3['QuantityOnhand'] = bal
                                                    flag1 = 0
                                try:
                                    temp_df=temp_df.drop([k])
                                    temp_df2 = temp_df2.append(split1, ignore_index=True)
                                    temp_df2 = temp_df2.append(split2, ignore_index=True)
                                    temp_df2 = temp_df2.append(split3, ignore_index=True)
                                except:
                                    pass
                        elif to_Give_qty > 0:
                            flag2 = 1
                            for key, val in to_Give.items(): 
                                if flag2 ==1:
                                    if val <= 0:
                                        pass
                                    else:
                                        if val >= int(row['QuantityOnhand']):
                                            val = val - int(row['QuantityOnhand'])
                                            to_Give[key] = val
                                            if temp_df.at[k,'DISPOSITION'] == 'READY TO DEPLOY':
                                                temp_df.at[k,'Disposition_Final'] = 'RTD_SUBSTITUTE'
                                            else:
                                                temp_df.at[k,'Disposition_Final'] = 'LAB_SUBSTITUTE'
    
                                            temp_df.at[k,'Destination'] = key
                                            flag2 = 0
                                            to_Give_qty = to_Give_qty - int(row['QuantityOnhand'])
                                        else:
                                            bal = int(row['QuantityOnhand']) - val
                                            to_Give_qty = to_Give_qty - val
                                            split1 = dict(row)
                                            split2 = dict(row)
                                            split1['QuantityOnhand'] = val
                                            to_Give[key] = 0
    
                                            if split1['DISPOSITION'] == 'READY TO DEPLOY':
                                                split1['Disposition_Final'] = 'RTD_SUBSTITUTE'
                                            else:
                                                split1['Disposition_Final'] = 'LAB_SUBSTITUTE'
                                            split1['Destination'] = key
    
                                            flag2 = 0
                                            if to_Give_qty <= 0:
                                                split2['QuantityOnhand'] = bal
                                            else:
                                                split2['QuantityOnhand'] = bal
    
                                                if split2['DISPOSITION'] == 'READY TO DEPLOY':
                                                    split2['Disposition_Final'] = 'RTD_SUBSTITUTE'
                                                else:
                                                    split2['Disposition_Final'] = 'LAB_SUBSTITUTE'
    
                                                a_next = list(to_Give.keys())
    
                                                for ind, u in enumerate(a_next):
                                                    if ind == len(a_next)-1:
                                                        res = key
                                                    else:
                                                        if u == key:
                                                            res = a_next[ind+1]
                                                            
                                                split2['Destination'] = res
                                                val2 = to_Give[res]
                                                to_Give[res] = val2 - bal
    
                                            try:
                                                temp_df=temp_df.drop([k])
                                                temp_df2 = temp_df2.append(split1, ignore_index=True)
                                                temp_df2 = temp_df2.append(split2, ignore_index=True)
                                            except:
                                                pass
            temp_df = temp_df.append(temp_df2, ignore_index=True)
            temp_df1 = temp_df1.append(temp_df, ignore_index=True)

    except Exception as err:
        issue_mod.append(j)
        
qty_sum_list = []
for it in non_inv_items_list:
    try:
        qty_sum = 0
        non_inv_items_df = temp_df1[temp_df1['Destination'] == it]
        qty_sum = np.sum(non_inv_items_df['QuantityOnhand'])
        qty_sum_list.append(qty_sum)
    except:
        qty_sum_list.append(0)

not_inv_df = demand[demand['ATTItemNumber'].isin(non_inv_items_list)][['ATTItemNumber','Demand_Future_12_Month','DaysUntilShortage','MarketPrice']]
not_inv_df['Substitution'] = qty_sum_list
not_inv_df['Qty_req_after_substitution'] = not_inv_df['Demand_Future_12_Month'] - not_inv_df['Substitution']

#temp_df1.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/temp_df1.xlsx")
#not_inv_df.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/not_inv_df.xlsx")

print("Substitution Logic | End Time-{}".format(datetime.now()))


# # Substitution Logic END

# # Data Preparation For Skynet

#%%

#not_inv_df.to_excel("/home/shubhamrelekar/Desktop/not_inv_df.xlsx")
#not_inv_df.to_excel('C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/not_inv_df_Sep_30th_2021.xlsx')


# In[10]:


#Qty Left After Substitution

print("Data Preparation For Skynet-1 | Start Time: {}".format(datetime.now()))

qty_sub = [] 
for itm in uniq_items:        #uniq_items
    itm_df = temp_df1[temp_df1['ATTItemNumber'] == itm]
    subQty = 0
    
    for k, row in itm_df.iterrows(): 
        if row['Item Delta'] >= 0:
            if (row['Disposition_Final'] == 'x') & (row['Destination'] == 'y'):
                subQty += int(row['QuantityOnhand'])
                
            else:
                subQty += 0


        elif row['Item Delta'] < 0:
            if row['Destination'] != row['ATTItemNumber']:
                subQty += int(row['QuantityOnhand']) 

            else:
                subQty += 0
    
    qty_sub.append(subQty)

                                            
after_sub_df = pd.DataFrame({'ATTItemNumber':uniq_items,'Qty Left After Substitution':qty_sub})
temp_df1 = temp_df1.merge(after_sub_df,on='ATTItemNumber',how='left')

print("Data Preparation For Skynet-1 | End Time: {}".format(datetime.now()))


# In[11]:


#Qty Required After Substitution
print("Data Preparation For Skynet-2 | Start Time: {}".format(datetime.now()))

after_sub_df = pd.DataFrame()
skynet_df = pd.DataFrame()
sort_df = pd.DataFrame()

sub_df1 = temp_df1[temp_df1['Destination'] == 'y']
complete_items = uniq_items + non_inv_items_list         
for itm in complete_items:
    total_qty_onhand = 0
    subQty = 0
    qty_sub = []
    itm_df1 = temp_df1[temp_df1['Destination'] == itm] 
    
    itm_df2 = itm_df1[itm_df1['ATTItemNumber'] == itm]
    DeltaMean = np.mean(itm_df2['Item Delta']) 
    substitute_row = itm_df1[itm_df1['Disposition_Final'].str.contains('_sub')]
#     total_qty_onhand = np.sum(substitute_row['QuantityOnhand'])
    
#     if DeltaMean >= 0:
#         subQty = 0
#     elif DeltaMean < 0:
#         subQty = -(abs(DeltaMean) - abs(total_qty_onhand))
    
    for k, row in itm_df1.iterrows():
        if row['Item Delta'] >= 0:
            subQty = 0 

        elif row['Item Delta'] < 0:
            total_qty_onhand = np.sum(substitute_row['QuantityOnhand'])
            subQty = -(abs(DeltaMean) - abs(total_qty_onhand))
                        
        qty_sub.append(subQty)
    
    itm_df1['Qty Required After Substitution'] = qty_sub    
    after_sub_df = after_sub_df.append(itm_df1, sort = False)

skynet_df = pd.concat([after_sub_df, sub_df1])
skynet_df = skynet_df.fillna(0)


for it in uniq_items:  
    it_df1 = skynet_df[skynet_df['ATTItemNumber'] == it]
    it_df1 = it_df1.sort_values(['MD_Priority','Aging','QuantityOnhand'],ascending=[True,True,False])
    sort_df = sort_df.append(it_df1)

#sort_df.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/sort_df.xlsx")    
print("Data Preparation For Skynet-2 | End Time: {}".format(datetime.now()))


# # Component Skynet Logic

# In[26]:


df_nd_comp = sort_df[sort_df['Is_Parent'] == 'comp']
comp_list = list(set(df_nd_comp['ATTItemNumber']))


# In[30]:


print("Component Skynet Logic | Start Time: {}".format(datetime.now()))

final_comp_skynet_df = pd.DataFrame()

for i in comp_list:
    parent_qty_req_aft_sub = []
    bomRatio = []
    parent_days_until_shortage = []
    parent_market_price = []
    emp_df = pd.DataFrame()
    par_data_dict = {}
    
    comp_df = sort_df[sort_df['ATTItemNumber'] == i]
    mean_qty_left_aft_subs = int(np.mean(comp_df['Qty Left After Substitution']))
    
    if mean_qty_left_aft_subs <= 0:
        final_comp_skynet_df = final_comp_skynet_df.append(comp_df,ignore_index=True)
        continue
        
    temp_bom = bom[bom['ComponentATTItem'] == i]
    if temp_bom.empty:
        final_comp_skynet_df = final_comp_skynet_df.append(comp_df,ignore_index=True)
        continue
    else: 
        otherParSet = set(temp_bom['ParentATTItem']) 
        emp_df['Parents'] = list(otherParSet)
        
        for p in otherParSet: 
            temp_bom_2 = bom[(bom['ComponentATTItem'] == i) & (bom['ParentATTItem'] == p)]
            try:
                bomRatio.append(int(temp_bom_2['BOMRatioQty']))
            except:
                bomRatio.append(0)
            
            par_df = sort_df[sort_df['ATTItemNumber'] == p]
            
            if par_df.empty:
                dem_df = not_inv_df[not_inv_df['ATTItemNumber'] == p] 
                dem_df['DaysUntilShortage'] = dem_df['DaysUntilShortage'].replace(['Critical Shortage'],0)
                dem_df['DaysUntilShortage'] = dem_df['DaysUntilShortage'].replace(['No Shortage'],99999)
                
                dem_df = dem_df.fillna(0)
                dem_df['MarketPrice'] = dem_df['MarketPrice'].replace('\s+', '', regex=True).replace('[,]', '', regex=True)
                #dem_df['MarketPrice'] = pd.to_numeric(dem_df['MarketPrice'])
                parent_qty_req_aft_sub.append(np.mean(dem_df['Qty_req_after_substitution']))
                parent_days_until_shortage.append(np.mean(dem_df['DaysUntilShortage'].astype(int)))
                parent_market_price.append(np.mean(dem_df['MarketPrice'].astype(float).astype(int)))
            else:
                par_df['DaysUntilShortage'] = par_df['DaysUntilShortage'].replace(['Critical Shortage'],0)
                par_df['DaysUntilShortage'] = par_df['DaysUntilShortage'].replace(['No Shortage'],99999)
                
                par_df = par_df.fillna(0)
                par_df['MarketPrice'] = par_df['MarketPrice'].replace('\s+', '', regex=True).replace('[,]', '', regex=True)
                #par_df['MarketPrice'] = pd.to_numeric(par_df['MarketPrice'])
                parent_qty_req_aft_sub.append(np.mean(par_df['Qty Required After Substitution'].astype(int)))
                parent_days_until_shortage.append(np.mean(par_df['DaysUntilShortage'].astype(int)))
                parent_market_price.append(np.mean(par_df['MarketPrice'].astype(float).astype(int)))
            
    
        emp_df['Qty Required After Substitution'] = parent_qty_req_aft_sub
        emp_df['DaysUntilShortage'] = parent_days_until_shortage
        emp_df['MarketPrice'] = parent_market_price
        emp_df['bomRatio'] = bomRatio
        emp_df['Parent Requirement'] = emp_df['Qty Required After Substitution'] * emp_df['bomRatio']
        emp_df = emp_df.sort_values(['DaysUntilShortage','MarketPrice'],ascending=[True,False])
        emp_df = emp_df.fillna(0) 
        
        
        for c, row in emp_df.iterrows():
            par_data_dict[row['Parents']] = abs(row['Parent Requirement'])
        
        try:
            par_to_Give_qty = sum(par_data_dict.values())
        except:
            par_to_Give_qty = 0
        
        skynet_df = pd.DataFrame()
        
        for i,data in comp_df.iterrows():
            try:
                del(split1)
                del(split2)
            except:
                pass    
                
            flag1 = 1
            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if par_to_Give_qty > 0:
                    for key, val in par_data_dict.items():
                        if flag1 == 1:
                            if val == 0: 
                                pass
                            else:
                                if data['QuantityOnhand'] <= val:
                                    comp_df.at[i,'Disposition_Final'] = 'SKYNET'
                                    comp_df.at[i,'Destination'] = key
                                    par_to_Give_qty = par_to_Give_qty - int(data['QuantityOnhand'])
                                    par_data_dict[key] = val - int(data['QuantityOnhand'])
                                    flag1 = 0
                                    break
    
                                else:
                                    bal = data['QuantityOnhand'] - val
                                    split1 = dict(data)
                                    split1['QuantityOnhand'] = val 
                                    split1['Disposition_Final'] = 'SKYNET'
                                    split1['Destination'] = key
    
                                    split2 = dict(data)
    
                                    par_to_Give_qty = par_to_Give_qty - val
                                    par_data_dict[key] = 0 
                                    flag1 = 0
    
                                    if par_to_Give_qty <= 0:
                                        split2['QuantityOnhand'] = bal
                                    else:
                                        split2['QuantityOnhand'] = bal  
    
                                        a_next = list(par_data_dict.keys())                           
                                        
                                        for ind, u in enumerate(a_next):
                                            if ind == len(a_next)-1:
                                                res = key
                                            else:
                                                if u == key:
                                                    res = a_next[ind+1]
    
                                        if par_data_dict[res] > 0:
                                            split2['Destination'] = res
                                            val2 = par_data_dict[res]
                                            split2['Disposition_Final'] = 'SKYNET'
                                            par_data_dict[res] = val2 - bal 
    
    
                                    try:
                                        comp_df=comp_df.drop([i])
                                        skynet_df = skynet_df.append(split1, ignore_index=True)
                                        skynet_df = skynet_df.append(split2, ignore_index=True)
                                    except:
                                        pass 
                            
        comp_df = comp_df.append(skynet_df, ignore_index=True)                    
        final_comp_skynet_df = final_comp_skynet_df.append(comp_df,ignore_index=True)

comp_skynet_sort_df = pd.DataFrame()      
for cm in comp_list:
    cm_df1 = final_comp_skynet_df[final_comp_skynet_df['ATTItemNumber'] == cm]
    cm_df1 = cm_df1.sort_values(['MD_Priority','Aging','QuantityOnhand'],ascending=[True,True,False])
    comp_skynet_sort_df = comp_skynet_sort_df.append(cm_df1)



skynet_qty_sum_list = []
for it in non_inv_items_list:
    try:
        skynet_qty_sum = 0
        non_inv_items_skynet_df = comp_skynet_sort_df[comp_skynet_sort_df['Destination'] == it and comp_skynet_sort_df['Disposition_Final'] == 'SKYNET']
        skynet_qty_sum = np.sum(non_inv_items_skynet_df['QuantityOnhand'])
        skynet_qty_sum_list.append(skynet_qty_sum)
    except:
        skynet_qty_sum_list.append(0)

not_inv_skynet_df = demand[demand['ATTItemNumber'].isin(non_inv_items_list)][['ATTItemNumber','Demand_Future_12_Month','DaysUntilShortage','MarketPrice']]
not_inv_df['Comp Skynet'] = skynet_qty_sum_list
not_inv_df['Qty_req_after_comp_skynet'] = not_inv_df['Qty_req_after_substitution'] - not_inv_df['Comp Skynet']


print("Component Skynet Logic | End Time: {}".format(datetime.now()))


# # Component Skynet Logic END

# # Component Safety Net and Liquidate

# In[31]:


print("Component Safety Net and Liquidate | Start Time: {}".format(datetime.now()))

comp_skynet_sort_df['Model_Safety_Net'] = np.where(comp_skynet_sort_df.Model == 'N-A',0,
                    np.where(comp_skynet_sort_df.Model_Demand_Past_12_Month > comp_skynet_sort_df.Model_Demand_Future_12_Month,
                             3*comp_skynet_sort_df.Model_Demand_Past_12_Month, 3*comp_skynet_sort_df.Model_Demand_Future_12_Month))

comp_skynet_sort_df = comp_skynet_sort_df.append(ms_integrated,ignore_index=True)
ext_int_comp_items = set(list(comp_skynet_sort_df["ATTItemNumber"]))
WWTPartCla_Pri = pd.DataFrame({'WWTPartClassification': ['Standalone','External Component','Integrated Component'],
                 'PartClass_Priority': [1,2,3]})
comp_skynet_sort_df = comp_skynet_sort_df.merge(WWTPartCla_Pri,on="WWTPartClassification", how='left')

ext_int_comp_skynet_sort_df = pd.DataFrame()
for eic in ext_int_comp_items:  
    eic_df1 = comp_skynet_sort_df[comp_skynet_sort_df['ATTItemNumber'] == eic]
    eic_df1 = eic_df1.sort_values(['PartClass_Priority','MD_Priority','Aging','QuantityOnhand'],ascending=[True,True,True,False])
    ext_int_comp_skynet_sort_df = ext_int_comp_skynet_sort_df.append(eic_df1)
    
final_comp_df = pd.DataFrame()

for c in ext_int_comp_items:
    keep_qty = 0
    sn_df2 = pd.DataFrame() 
    sn_df = ext_int_comp_skynet_sort_df[ext_int_comp_skynet_sort_df["ATTItemNumber"]==c]
    model_safety_net = int(np.mean(sn_df['Model_Safety_Net']))
        
    keep_qty_data = len(keep_list.loc[keep_list['Item'] == c,'Keep Quantity'].values)
    
    if keep_qty_data > 0:
        keep_qty = keep_list.loc[keep_list['Item'] == c,'Keep Quantity'].values[0] 
        for i,data in sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if int(keep_qty) > 0 :
                    if keep_qty >= data['QuantityOnhand']:
                        keep_qty = keep_qty - data['QuantityOnhand']
                        sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                        sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                    else:
                        bal = data['QuantityOnhand'] - keep_qty
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = keep_qty
                        split1['Disposition_Final'] = 'KEEP'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        keep_qty = 0
                        
                        split2 = dict(data)                    
                        
                        if model_safety_net > 0:
                            if bal <= model_safety_net: 
                                split2['QuantityOnhand'] = bal
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                model_safety_net = model_safety_net - bal
                            else:
                                bal2 = bal - model_safety_net
                                split2['QuantityOnhand'] = model_safety_net
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                model_safety_net = 0

                                split3 = dict(data)
                                split3['QuantityOnhand'] = bal2
                                split3['Disposition_Final'] = 'LIQUIDATE'
                                split3['Destination'] = 'LIQUIDATE'
                        else:
                            split2['QuantityOnhand'] = bal
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'
                            
                        try:
                            sn_df=sn_df.drop([i])
                            sn_df2 = sn_df2.append(split1, ignore_index=True)
                            sn_df2 = sn_df2.append(split2, ignore_index=True)
                            sn_df2 = sn_df2.append(split3, ignore_index=True)
                        except:
                            pass
                
 
                elif model_safety_net > 0:
                    if model_safety_net >= data['QuantityOnhand']:
                        sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                        sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        model_safety_net = model_safety_net - data['QuantityOnhand']
                    else:
                        bal = data['QuantityOnhand'] - model_safety_net
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = model_safety_net
                        split1['Disposition_Final'] = 'SAFETY NET'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        model_safety_net = 0 

                        split2 = dict(data)
                        split2['QuantityOnhand'] = bal
                        split2['Disposition_Final'] = 'LIQUIDATE'
                        split2['Destination'] = 'LIQUIDATE'

                        try:
                            sn_df=sn_df.drop([i])
                            sn_df2 = sn_df2.append(split1, ignore_index=True)
                            sn_df2 = sn_df2.append(split2, ignore_index=True)
                        except:
                            pass 

                else:
                    sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                    sn_df.at[i, 'Destination'] = 'LIQUIDATE' 
        
    else:    
        for i,data in sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if data['ExternalDownloadFlag'] not in(['B','X']):
                    sn_df.at[i, 'Disposition_Final'] = 'NOT TO LIQUIDATE - Ext Dwld Flg'
                    sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                else: 
                    if int(keep_qty) > 0 :
                        if keep_qty >= data['QuantityOnhand']:
                            keep_qty = keep_qty - data['QuantityOnhand']
                            sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                            sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        else:
                            bal = data['QuantityOnhand'] - keep_qty
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = keep_qty
                            split1['Disposition_Final'] = 'KEEP'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            keep_qty = 0
                            
                            split2 = dict(data)
                            
                            if model_safety_net > 0:
                                if bal <= model_safety_net:
                                    split2['QuantityOnhand'] = bal
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    model_safety_net = model_safety_net - bal
                                else:
                                    bal2 = bal - model_safety_net
                                    split2['QuantityOnhand'] = model_safety_net
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    model_safety_net = 0

                                    split3 = dict(data)
                                    split3['QuantityOnhand'] = bal2
                                    split3['Disposition_Final'] = 'LIQUIDATE'
                                    split3['Destination'] = 'LIQUIDATE'
                            
                            else:
                                split2['QuantityOnhand'] = bal
                                split2['Disposition_Final'] = 'LIQUIDATE'
                                split2['Destination'] = 'LIQUIDATE'
                            
                            try:
                                sn_df=sn_df.drop([i])
                                sn_df2 = sn_df2.append(split1, ignore_index=True)
                                sn_df2 = sn_df2.append(split2, ignore_index=True)
                                sn_df2 = sn_df2.append(split3, ignore_index=True)
                            except:
                                pass
                    
                    elif model_safety_net > 0:
                        if model_safety_net >= data['QuantityOnhand']:
                            sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                            sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                            model_safety_net = model_safety_net - data['QuantityOnhand']
                        else:
                            bal = data['QuantityOnhand'] - model_safety_net
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = model_safety_net
                            split1['Disposition_Final'] = 'SAFETY NET'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            model_safety_net = 0 

                            split2 = dict(data)
                            split2['QuantityOnhand'] = bal
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'

                            try:
                                sn_df=sn_df.drop([i])
                                sn_df2 = sn_df2.append(split1, ignore_index=True)
                                sn_df2 = sn_df2.append(split2, ignore_index=True)
                            except:
                                pass 

                    else:
                        sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                        sn_df.at[i, 'Destination'] = 'LIQUIDATE'     
                
                
    sn_df = sn_df.append(sn_df2, ignore_index=True)
    final_comp_df = final_comp_df.append(sn_df, ignore_index=True)

#final_comp_df.to_excel('/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/allexcel_files/final_Comp_df.xlsx')

print("Component Safety Net and Liquidate | End Time: {}".format(datetime.now()))


# In[32]:


Final_Df = Final_Df.append(final_comp_df, ignore_index=True)


# # Component Safety Net and Liquidate END

# # Parent Skynet Logic

# In[33]:


df_nd_par = sort_df[sort_df['Is_Parent'] == 'par']
par_list = list(set(df_nd_par['ATTItemNumber']))


# In[34]:


print("Parent Skynet Logic | Start Time: {}".format(datetime.now()))

comp_par_skynet_df = pd.DataFrame()
par_df = pd.DataFrame()
parent_qty = []
parent_item = []
par_qty_left_chk = pd.DataFrame()
comp_extract = pd.DataFrame()
final_par_skynet_df = pd.DataFrame()


for j in par_list:
    skynet_sum = 0
    try:
        comp_par_skynet_df = final_comp_df[final_comp_df['Destination'] == j]
        comp_par_skynet_set = list(set(comp_par_skynet_df['ATTItemNumber']))
        
        for cs in comp_par_skynet_set:
            bom_ratio = bom.loc[(bom['ParentATTItem'] == j) & (bom['ComponentATTItem'] == cs) ,'BOMRatioQty'].values[0]
            cs_df = comp_par_skynet_df[comp_par_skynet_df['ATTItemNumber'] == cs]
            s_sum = math.ceil(np.sum(cs_df['QuantityOnhand']) / bom_ratio)
            skynet_sum += s_sum
    except:
        pass
    
    par_df = sort_df[sort_df['ATTItemNumber'] == j]
    qty_req_after_sub = np.mean(par_df['Qty Required After Substitution'])
    qty_after_comp_skynet = abs(qty_req_after_sub) - skynet_sum
    
    parent_qty.append(qty_after_comp_skynet)
    parent_item.append(j)

parent_skynet_req = pd.DataFrame({'ATTItemNumber':parent_item, 'Parent Qty Req After Comp Skynet':parent_qty})

df_nd_par = df_nd_par.merge(parent_skynet_req, on='ATTItemNumber', how='left')

for k in par_list: 
    par_qty_left_chk = df_nd_par[df_nd_par['ATTItemNumber'] == k]
    par_qty_left_mean = int(np.mean(par_qty_left_chk['Qty Left After Substitution']))
    
    if par_qty_left_mean <= 0:
        final_par_skynet_df = final_par_skynet_df.append(par_qty_left_chk,ignore_index=True)
        continue
    
    else:
        temp_bom = bom[bom['ParentATTItem'] == k]
        temp_bom = temp_bom[(temp_bom["ComponentATTItem"]!="TBUY")] 
        
        if temp_bom.empty:
            final_par_skynet_df = final_par_skynet_df.append(par_qty_left_chk,ignore_index=True)
            continue
        else:
            temp_bom.rename(columns = {'BOMRatioQty':'Org Par Bom Ratio'}, inplace = True)            
            CompSet = list(set(temp_bom['ComponentATTItem']))
            par_comp_skynet = pd.DataFrame()

            for c in CompSet:
                par_dus_list = []
                par_qty_comp_skynet_list = []
                par_mkt_price_list = []
                par_dus_df = pd.DataFrame()

                temp_bom_comp = bom[bom['ComponentATTItem'] == c]
                comp_extract = temp_bom_comp[['ComponentATTItem', 'ParentATTItem', 'BOMRatioQty']].copy()
                parattitem_list = list(set(comp_extract['ParentATTItem'].astype(object)))
                
                for p in parattitem_list:
                    par_dus_df = df_nd_par[df_nd_par['ATTItemNumber'] == p]
                    
                    if par_dus_df.empty:
                        par_dem_df = not_inv_df[not_inv_df['ATTItemNumber'] == p]
                        par_dem_df['DaysUntilShortage'] = par_dem_df['DaysUntilShortage'].replace(['Critical Shortage'],0)
                        par_dem_df['DaysUntilShortage'] = par_dem_df['DaysUntilShortage'].replace(['No Shortage'],99999)
                        
                        par_dem_df = par_dem_df.fillna(0)
                        par_dem_df['MarketPrice'] = par_dem_df['MarketPrice'].replace('\s+', '', regex=True).replace('[,]', '', regex=True)
                        par_qty_comp_skynet_list.append(np.mean(par_dem_df['Qty_req_after_comp_skynet'].astype(int)))
                        par_dus_list.append(np.mean(par_dem_df['DaysUntilShortage'].astype(int)))
                        par_mkt_price_list.append(np.mean(par_dem_df['MarketPrice'].astype(float).astype(int)))
                    
                    else:
                        par_dus_df['DaysUntilShortage'] = par_dus_df['DaysUntilShortage'].replace(['Critical Shortage'],0)
                        par_dus_df['DaysUntilShortage'] = par_dus_df['DaysUntilShortage'].replace(['No Shortage'],99999)
                        
                        par_dus_df = par_dus_df.fillna(0)
                        par_dus_df['MarketPrice'] = par_dus_df['MarketPrice'].replace('\s+', '', regex=True).replace('[,]', '', regex=True)
                        par_dus_list.append(np.mean(par_dus_df['DaysUntilShortage'].astype(int)))
                        par_qty_comp_skynet_list.append(np.mean(par_dus_df['Parent Qty Req After Comp Skynet'].astype(int)))
                        par_mkt_price_list.append(np.mean(par_dus_df['MarketPrice'].astype(float).astype(int)))

                parent_comp_df = pd.DataFrame({'ParentATTItem':parattitem_list,'Parent DaysUntilShortage':par_dus_list,
                                               'Parent Qty Req After Comp Skynet':par_qty_comp_skynet_list,
                                               'Parent Market Price':par_mkt_price_list}, dtype='object')
                
                comp_extract = comp_extract.merge(parent_comp_df, on="ParentATTItem", how="left")
                
                par_comp_skynet = par_comp_skynet.append(comp_extract)
                
            
            par_comp_skynet = par_comp_skynet.merge(temp_bom[['ComponentATTItem','Org Par Bom Ratio']], on='ComponentATTItem', how='left')
            par_comp_skynet = par_comp_skynet.sort_values(['Parent DaysUntilShortage', 'Parent Qty Req After Comp Skynet', 'Parent Market Price'], ascending=[True, False, False])

            skynet_dest_dict = {}
            
            par_comp_skynet = par_comp_skynet.fillna(0)
            for n, pc in par_comp_skynet.iterrows():
                skynet_dest_dict_key = "{0}_{1}".format(pc['ComponentATTItem'],pc['ParentATTItem'])
                skynet_dest_dict_val = "{}".format(math.ceil((int(pc['BOMRatioQty']) * int(pc['Parent Qty Req After Comp Skynet'])) / pc['Org Par Bom Ratio']))
                skynet_dest_dict[skynet_dest_dict_key] = skynet_dest_dict_val

            try:
                par_qty_for_skynet = sum(skynet_dest_dict.values())
            except:
                par_qty_for_skynet = 0


            par_skynet_df = pd.DataFrame()

            for i,data in par_qty_left_chk.iterrows():
                try:
                    del(split1)
                    del(split2)
                except:
                    pass    

                flag1 = 1

                if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                    if par_qty_for_skynet > 0:

                        for key, val in skynet_dest_dict.items():
                            if flag1 == 1:
                                if val == 0: 
                                    pass
                                else:
                                    if data['QuantityOnhand'] <= val:
                                        par_qty_left_chk.at[i,'Disposition_Final'] = 'SKYNET'
                                        par_qty_left_chk.at[i,'Destination'] = key
                                        par_qty_for_skynet = par_qty_for_skynet - int(data['QuantityOnhand'])
                                        skynet_dest_dict[key] = val - int(data['QuantityOnhand'])
                                        flag1 = 0
                                        break

                                    else:
                                        bal = data['QuantityOnhand'] - val
                                        split1 = dict(data)
                                        split1['QuantityOnhand'] = val 
                                        split1['Disposition_Final'] = 'SKYNET'
                                        split1['Destination'] = key

                                        split2 = dict(data)

                                        par_qty_for_skynet = par_qty_for_skynet - val
                                        skynet_dest_dict[key] = 0 
                                        flag1 = 0

                                        if par_qty_for_skynet <= 0:
                                            split2['QuantityOnhand'] = bal
                                        else:
                                            split2['QuantityOnhand'] = bal  

                                            a_next = list(skynet_dest_dict.keys())

                                            for ind, u in enumerate(a_next):
                                                if ind == len(a_next)-1:
                                                    res = key
                                                else:
                                                    if u == key:
                                                        res = a_next[ind+1]

                                            if skynet_dest_dict[res] > 0:
                                                split2['Destination'] = res
                                                val2 = skynet_dest_dict[res]
                                                split2['Disposition_Final'] = 'SKYNET'
                                                skynet_dest_dict[res] = val2 - bal 


                                        try:
                                            par_qty_left_chk=par_qty_left_chk.drop([i])
                                            par_skynet_df = par_skynet_df.append(split1, ignore_index=True)
                                            par_skynet_df = par_skynet_df.append(split2, ignore_index=True)
                                        except:
                                            pass 

            par_qty_left_chk = par_qty_left_chk.append(par_skynet_df, ignore_index=True) 
            final_par_skynet_df = final_par_skynet_df.append(par_qty_left_chk,ignore_index=True)

try:   
    
    par_skynet_sort_df = pd.DataFrame()      
    for pr in par_list:
        pr_df1 = final_par_skynet_df[final_par_skynet_df['ATTItemNumber'] == pr]
        pr_df1 = pr_df1.sort_values(['MD_Priority','Aging','QuantityOnhand'],ascending=[True,True,False])
        par_skynet_sort_df = par_skynet_sort_df.append(pr_df1)
    
    
    par_skynet_qty_sum_list = []
    for it in non_inv_items_list:
        try:
            par_skynet_qty_sum = 0
            par_non_inv_items_skynet_df = par_skynet_sort_df[par_skynet_sort_df['Destination'] == it and par_skynet_sort_df['Disposition_Final'] == 'SKYNET']
            par_skynet_qty_sum = np.sum(par_non_inv_items_skynet_df['QuantityOnhand'])
            par_skynet_qty_sum_list.append(par_skynet_qty_sum)
        except:
            par_skynet_qty_sum_list.append(0)
    
    #not_inv_skynet_df = demand[demand['ATTItemNumber'].isin(non_inv_items_list)][['ATTItemNumber','Demand_Future_12_Month','DaysUntilShortage','MarketPrice']]
    not_inv_df['Par Skynet'] = par_skynet_qty_sum_list
    not_inv_df['Qty_req_after_par_skynet'] = not_inv_df['Qty_req_after_comp_skynet'] - not_inv_df['Par Skynet']


except KeyError as k:
    print("Key not available. {}".format(k))
    
#not_inv_df.to_excel('C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/not_inv_df_9.xlsx')

print("Parent Skynet Logic | End Time: {}".format(datetime.now()))


# # Parent Skynet Logic END



#%%
# # BOM Parent Liquidate
par_df_new = pd.DataFrame()
k_desig = ['ATT-K - C','ATTKSTOCK - C','ATTAP/K - C','GCRMAKSTOCK - C','GCRMAOEM-K - C']
for bpl in par_list:
    par_desig = []
    bpl_df = par_skynet_sort_df[par_skynet_sort_df['ATTItemNumber'] == bpl]
    bpl_df_new = bpl_df[(bpl_df.Disposition_Final == "x") & (bpl_df.Destination == "y")]
    distinct_desig = list(set(bpl_df_new['MaterialDesignator']))
     
    for d in distinct_desig:
        if d in k_desig:
            par_desig.append(d)
        else:
            continue
    
    if len(par_desig) == 0:
        par_df_new = par_df_new.append(bpl_df, ignore_index=True)
        continue
    else:
        #pivot_par=pd.pivot_table(bpl_df_new,values=['QuantityOnhand'],index=['ATTItemNumber','MaterialDesignator','DISPOSITION'],aggfunc=np.mean)
        #pivot_par['tmp'] =  pivot_par.index 
        #pivot_par[['ATTItemNumber','MaterialDesignator','DISPOSITION']] = pd.DataFrame(pivot_par['tmp'].tolist(), index=pivot_par.index)
        #pivot_par.drop('tmp', axis='columns', inplace=True)
        #pivot_par.index = range(0,len(pivot_par['ATTItemNumber']))
        
        bom_par_lqdt = bom[bom['ParentATTItem'] == bpl]
        bom_par_lqdt= bom_par_lqdt[(bom_par_lqdt["ComponentATTItem"]!="TBUY")] 
        
        if bom_par_lqdt.empty:
            for i, kpar in bpl_df.iterrows():
                if kpar['Disposition_Final'] == 'x' and kpar['Destination'] == 'y':
                    if kpar['MaterialDesignator'] in par_desig:
                        bpl_df.at[i, 'Disposition_Final'] = 'NOT TO LIQUIDATE - No Comp Liq'
                        bpl_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                    else:
                        continue
            par_df_new = par_df_new.append(bpl_df,ignore_index=True)
            
        else:
            comp_lqdt = list(set(bom_par_lqdt['ComponentATTItem']))
            MD_Dict = {}
            Inv_Dict = {}            
            for desig in par_desig:
                inv_loc_df = bpl_df_new[bpl_df_new.MaterialDesignator == desig]
                inv_loc_id = list(set(inv_loc_df['InventoryLocationId']))
                for inv in inv_loc_id:
                    comp_desig_qty = []
                    for comp in comp_lqdt:
                        k_comp_df = pd.DataFrame()
                        bom_lqdt_df = bom_par_lqdt[bom_par_lqdt['ComponentATTItem']==comp]
                        bom_lqdt_ratio = bom_lqdt_df['BOMRatioQty']
                        k_comp_df = final_comp_df[(final_comp_df['ATTItemNumber'] == comp)&(final_comp_df['MaterialDesignator'] == desig)
                                                  &(final_comp_df['Disposition_Final'] == 'LIQUIDATE')&(final_comp_df['InventoryLocationId'] == inv)]
                        
                        if not k_comp_df.empty:
                            comp_desig_qty.append(math.ceil(np.sum(k_comp_df['QuantityOnhand']) / bom_lqdt_ratio))
                        else:
                            break
                
                    if len(comp_lqdt) == len(comp_desig_qty):
                        Inv_Dict[inv] = min(comp_desig_qty)
                    else:
                        Inv_Dict[inv] = 0
                
                MD_Dict[desig] = Inv_Dict
                # if len(comp_lqdt) == len(comp_desig_qty):
                #     MD_Dict[desig] = min(comp_desig_qty)
                # else:
                #     MD_Dict[desig] = 0
                
                
#                print("------------------------------------------------")
#                print("MD_Dict-{}".format(MD_Dict))
#                print("desig: {}".format(desig))
#                print("------------------------------------------------")
#                
#                
#                if MD_Dict[desig] == 0:
#                    continue
#                else:
#                    MD_Dict[desig] = min(comp_desig_qty)
                #par_qty_to_lqdt = min(comp_desig_qty)
                
                
            temp_par_df = pd.DataFrame()
            for i, data in bpl_df.iterrows():
                try:
                    del(split1)
                    del(split2)
                except:
                    pass
                if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                    if data['MaterialDesignator'] in par_desig:
                        par_qty_to_lqdt = MD_Dict[data['MaterialDesignator']]
                        for key,val in par_qty_to_lqdt.items():
                            if (data['InventoryLocationId'] == key):
                                if val > 0:
                                    if data['QuantityOnhand'] <= val:
                                        val = val - data['QuantityOnhand']
                                        par_qty_to_lqdt[key] = val
                                        MD_Dict[data['MaterialDesignator']] = par_qty_to_lqdt
                                        bpl_df.at[i,'Disposition_Final'] = 'LIQUIDATE'
                                        bpl_df.at[i,'Destination'] = 'LIQUIDATE'
                                        break
                                    else:
                                        split1 = dict(data)
                                        bal = data['QuantityOnhand'] - val
                                        split1['Disposition_Final'] = 'LIQUIDATE'
                                        split1['Destination'] = 'LIQUIDATE'
                                        split1['QuantityOnhand'] = val
                                        val = 0
                                        par_qty_to_lqdt[key] = val
                                        MD_Dict[data['MaterialDesignator']] = par_qty_to_lqdt
                                        split2 = dict(data)
                                        split2['QuantityOnhand'] = bal
                                        split2['Disposition_Final'] = 'NOT TO LIQUIDATE - No Comp Liq'
                                        split2['Destination'] = 'ON HAND INVENTORY'
                                        
                                        try:
                                            bpl_df=bpl_df.drop([i])
                                            temp_par_df = temp_par_df.append(split1, ignore_index=True)
                                            temp_par_df = temp_par_df.append(split2, ignore_index=True)
                                        except:
                                            pass
                                        break
                                else:
                                    bpl_df.at[i,'Disposition_Final'] = 'NOT TO LIQUIDATE - No Comp Liq'
                                    bpl_df.at[i,'Destination'] = 'ON HAND INVENTORY'
                            else:
                                continue
                    else:
                        continue
                        
            bpl_df = bpl_df.append(temp_par_df, ignore_index = True)
            par_df_new = par_df_new.append(bpl_df, ignore_index = True)

par_df_new_sort = pd.DataFrame()      
for par in par_list:
    par_df1 = par_df_new[par_df_new['ATTItemNumber'] == par]
    par_df1 = par_df1.sort_values(['MD_Priority','Aging','QuantityOnhand'],ascending=[True,True,False])
    par_df_new_sort = par_df_new_sort.append(par_df1)                        
                  
#par_df_new_sort.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/par_df_new_sort_1.xlsx")
#final_comp_df.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/final_comp_df_1.xlsx")
# In[35]:

# # Parent Safety Net and Liquidate

print("Parent Safety Net and Liquidate | Start Time: {}".format(datetime.now()))

par_df_new_sort['Model_Safety_Net'] = np.where(par_df_new_sort.Model == 'N-A',0,
                    np.where(par_df_new_sort.Model_Demand_Past_12_Month > par_df_new_sort.Model_Demand_Future_12_Month,
                             3*par_df_new_sort.Model_Demand_Past_12_Month, 3*par_df_new_sort.Model_Demand_Future_12_Month))



final_par_df = pd.DataFrame() 

for p in par_list:
    par_keep_qty = 0
    par_sn_df2 = pd.DataFrame() 
    
    par_sn_df = par_df_new_sort[par_df_new_sort["ATTItemNumber"]==p]
    par_model_safety_net = np.mean(par_sn_df['Model_Safety_Net'])  
    par_keep_qty_data = len(keep_list.loc[keep_list['Item'] == p,'Keep Quantity'].values)
    
    if par_keep_qty_data > 0:
        par_keep_qty = keep_list.loc[keep_list['Item'] == p,'Keep Quantity'].values[0] 
        
        for i,data in par_sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if int(par_keep_qty) > 0 :
                    if par_keep_qty >= data['QuantityOnhand']:
                        par_keep_qty = par_keep_qty - data['QuantityOnhand']
                        par_sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                        par_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                    else:
                        bal = data['QuantityOnhand'] - par_keep_qty
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = par_keep_qty
                        split1['Disposition_Final'] = 'KEEP'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        par_keep_qty = 0
                        
                        split2 = dict(data)
                        
                        if par_model_safety_net > 0:
                            if bal <= par_model_safety_net:
                                split2['QuantityOnhand'] = bal
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                par_model_safety_net = par_model_safety_net - bal
                            else:
                                bal2 = bal - par_model_safety_net
                                split2['QuantityOnhand'] = par_model_safety_net
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                par_model_safety_net = 0

                                split3 = dict(data)
                                split3['QuantityOnhand'] = bal2
                                split3['Disposition_Final'] = 'LIQUIDATE'
                                split3['Destination'] = 'LIQUIDATE'
                                
                        else:
                            split2['QuantityOnhand'] = bal
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'
                        try:
                            par_sn_df=par_sn_df.drop([i])
                            par_sn_df2 = par_sn_df2.append(split1, ignore_index=True)
                            par_sn_df2 = par_sn_df2.append(split2, ignore_index=True)
                            par_sn_df2 = par_sn_df2.append(split3, ignore_index=True)
                        except:
                            pass                                    
                
                elif par_model_safety_net > 0:
                    if par_model_safety_net >= data['QuantityOnhand']:
                        par_sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                        par_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        par_model_safety_net = par_model_safety_net - data['QuantityOnhand']
                    else:
                        bal = data['QuantityOnhand'] - par_model_safety_net
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = par_model_safety_net
                        split1['Disposition_Final'] = 'SAFETY NET'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        par_model_safety_net = 0 

                        split2 = dict(data)
                        split2['QuantityOnhand'] = bal
                        split2['Disposition_Final'] = 'LIQUIDATE'
                        split2['Destination'] = 'LIQUIDATE'

                        try:
                            par_sn_df=par_sn_df.drop([i])
                            par_sn_df2 = par_sn_df2.append(split1, ignore_index=True)
                            par_sn_df2 = par_sn_df2.append(split2, ignore_index=True)
                        except:
                            pass 

                else:
                    par_sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                    par_sn_df.at[i, 'Destination'] = 'LIQUIDATE' 
        
    else:    
        for i,data in par_sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if not data['ExternalDownloadFlag'] in(['B','X']):
                    par_sn_df.at[i, 'Disposition_Final'] = 'NOT TO LIQUIDATE - Ext Dwld Flg'
                    par_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                else: 
                    if int(par_keep_qty) > 0 :
                        if par_keep_qty >= data['QuantityOnhand']:
                            par_keep_qty = par_keep_qty - data['QuantityOnhand']
                            par_sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                            par_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        else:
                            bal = data['QuantityOnhand'] - par_keep_qty
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = par_keep_qty
                            split1['Disposition_Final'] = 'KEEP'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            par_keep_qty = 0
                            
                            split2 = dict(data)
                            
                            if par_model_safety_net > 0:
                                if bal <= par_model_safety_net:
                                    
                                    split2['QuantityOnhand'] = bal
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    par_model_safety_net = par_model_safety_net - bal
                                else:
                                    bal2 = bal - par_model_safety_net
                                    split2['QuantityOnhand'] = par_model_safety_net
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    par_model_safety_net = 0

                                    split3 = dict(data)
                                    split3['QuantityOnhand'] = bal2
                                    split3['Disposition_Final'] = 'LIQUIDATE'
                                    split3['Destination'] = 'LIQUIDATE'
                            
                            else:
                                split2['QuantityOnhand'] = bal 
                                split2['Disposition_Final'] = 'LIQUIDATE'
                                split2['Destination'] = 'LIQUIDATE'
                            
                            try:
                                par_sn_df=par_sn_df.drop([i])
                                par_sn_df2 = par_sn_df2.append(split1, ignore_index=True)
                                par_sn_df2 = par_sn_df2.append(split2, ignore_index=True)
                                par_sn_df2 = par_sn_df2.append(split3, ignore_index=True)
                            except:
                                pass
                    
                    elif par_model_safety_net > 0:
                        if par_model_safety_net >= data['QuantityOnhand']:
                            par_sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                            par_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                            par_model_safety_net = par_model_safety_net - data['QuantityOnhand']
                        else:
                            bal = data['QuantityOnhand'] - par_model_safety_net
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = par_model_safety_net
                            split1['Disposition_Final'] = 'SAFETY NET'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            par_model_safety_net = 0 

                            split2 = dict(data)
                            split2['QuantityOnhand'] = bal
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'

                            try:
                                par_sn_df=par_sn_df.drop([i])
                                par_sn_df2 = par_sn_df2.append(split1, ignore_index=True)
                                par_sn_df2 = par_sn_df2.append(split2, ignore_index=True)
                            except:
                                pass 

                    else:
                        par_sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                        par_sn_df.at[i, 'Destination'] = 'LIQUIDATE'     
                
    
    par_sn_df = par_sn_df.append(par_sn_df2, ignore_index=True)
    final_par_df = final_par_df.append(par_sn_df, ignore_index=True)
    
#final_par_df.to_excel('/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/allexcel_files/safetyNet_Liquidate_df.xlsx')

print("Parent Safety Net and Liquidate | End Time: {}".format(datetime.now()))



# In[36]:


Final_Df = Final_Df.append(final_par_df, ignore_index=True)
#%%

#NA Safety Net and Liquidate

df_nd_na = sort_df[sort_df['Is_Parent'] == 'N-A']
na_list = list(set(df_nd_na['ATTItemNumber']))

#%%
print("NA Safety Net and Liquidate | Start Time: {}".format(datetime.now()))

df_nd_na['Model_Safety_Net'] = np.where(df_nd_na.Model == 'N-A',0,
                    np.where(df_nd_na.Model_Demand_Past_12_Month > df_nd_na.Model_Demand_Future_12_Month,
                             3*df_nd_na.Model_Demand_Past_12_Month, 3*df_nd_na.Model_Demand_Future_12_Month))


final_na_df = pd.DataFrame() 

for n in na_list:
    na_keep_qty = 0
    na_sn_df2 = pd.DataFrame() 
    
    na_sn_df = df_nd_na[df_nd_na["ATTItemNumber"]==n]
    na_model_safety_net = np.mean(na_sn_df['Model_Safety_Net'])  
        
    na_keep_qty_data = len(keep_list.loc[keep_list['Item'] == n,'Keep Quantity'].values)
    
    if na_keep_qty_data > 0:
        na_keep_qty = keep_list.loc[keep_list['Item'] == n,'Keep Quantity'].values[0] 
        
        for i,data in na_sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if int(na_keep_qty) > 0 :
                    if na_keep_qty >= data['QuantityOnhand']:
                        na_keep_qty = na_keep_qty - data['QuantityOnhand']
                        na_sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                        na_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                    else:
                        bal = data['QuantityOnhand'] - na_keep_qty
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = na_keep_qty
                        split1['Disposition_Final'] = 'KEEP'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        na_keep_qty = 0
                        
                        split2 = dict(data)
                            
                        if na_model_safety_net > 0: 
                            if bal <= na_model_safety_net: 
                                split2['QuantityOnhand'] = bal
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                na_model_safety_net = na_model_safety_net - bal
                            else:
                                bal2 = bal - na_model_safety_net
                                split2['QuantityOnhand'] = na_model_safety_net
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                na_model_safety_net = 0

                                split3 = dict(data)
                                split3['QuantityOnhand'] = bal2
                                split3['Disposition_Final'] = 'LIQUIDATE'
                                split3['Destination'] = 'LIQUIDATE'
                        
                        else:
                            split2['QuantityOnhand'] = bal 
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'
                        
                        try:
                            na_sn_df=na_sn_df.drop([i])
                            na_sn_df2 = na_sn_df2.append(split1, ignore_index=True)
                            na_sn_df2 = na_sn_df2.append(split2, ignore_index=True)
                            na_sn_df2 = na_sn_df2.append(split3, ignore_index=True)
                        except:
                            pass                    
                
                elif na_model_safety_net > 0:
                    if na_model_safety_net >= data['QuantityOnhand']:
                        na_sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                        na_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        na_model_safety_net = na_model_safety_net - data['QuantityOnhand']
                    else:
                        bal = data['QuantityOnhand'] - na_model_safety_net
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = na_model_safety_net
                        split1['Disposition_Final'] = 'SAFETY NET'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        na_model_safety_net = 0 

                        split2 = dict(data)
                        split2['QuantityOnhand'] = bal
                        split2['Disposition_Final'] = 'LIQUIDATE'
                        split2['Destination'] = 'LIQUIDATE'

                        try:
                            na_sn_df=na_sn_df.drop([i])
                            na_sn_df2 = na_sn_df2.append(split1, ignore_index=True)
                            na_sn_df2 = na_sn_df2.append(split2, ignore_index=True)
                        except:
                            pass 

                else:
                    na_sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                    na_sn_df.at[i, 'Destination'] = 'LIQUIDATE' 
        
    else:    
        for i,data in na_sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if not data['ExternalDownloadFlag'] in(['B','X']):
                    na_sn_df.at[i, 'Disposition_Final'] = 'NOT TO LIQUIDATE - Ext Dwld Flg'
                    na_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                else: 
                    if int(na_keep_qty) > 0 :
                        if na_keep_qty >= data['QuantityOnhand']:
                            na_keep_qty = na_keep_qty - data['QuantityOnhand']
                            na_sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                            na_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        else:
                            bal = data['QuantityOnhand'] - na_keep_qty
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = na_keep_qty
                            split1['Disposition_Final'] = 'KEEP'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            na_keep_qty = 0
                            
                            split2 = dict(data)
                            
                            if na_model_safety_net > 0:
                                if bal <= na_model_safety_net: 
                                    split2['QuantityOnhand'] = bal
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    na_model_safety_net = na_model_safety_net - bal
                                else:
                                    bal2 = bal - na_model_safety_net
                                    split2['QuantityOnhand'] = na_model_safety_net
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    na_model_safety_net = 0

                                    split3 = dict(data)
                                    split3['QuantityOnhand'] = bal2
                                    split3['Disposition_Final'] = 'LIQUIDATE'
                                    split3['Destination'] = 'LIQUIDATE'
                            
                            else:
                                split2['QuantityOnhand'] = bal 
                                split2['Disposition_Final'] = 'LIQUIDATE'
                                split2['Destination'] = 'LIQUIDATE'
                            
                            try:
                                na_sn_df=na_sn_df.drop([i])
                                na_sn_df2 = na_sn_df2.append(split1, ignore_index=True)
                                na_sn_df2 = na_sn_df2.append(split2, ignore_index=True)
                                na_sn_df2 = na_sn_df2.append(split3, ignore_index=True)
                            except:
                                pass                   
                    
                    elif na_model_safety_net > 0:
                        if na_model_safety_net >= data['QuantityOnhand']:
                            na_sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                            na_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                            na_model_safety_net = na_model_safety_net - data['QuantityOnhand']
                        else:
                            bal = data['QuantityOnhand'] - na_model_safety_net
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = na_model_safety_net
                            split1['Disposition_Final'] = 'SAFETY NET'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            na_model_safety_net = 0 

                            split2 = dict(data)
                            split2['QuantityOnhand'] = bal
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'

                            try:
                                na_sn_df=na_sn_df.drop([i])
                                na_sn_df2 = na_sn_df2.append(split1, ignore_index=True)
                                na_sn_df2 = na_sn_df2.append(split2, ignore_index=True)
                            except:
                                pass 

                    else:
                        na_sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                        na_sn_df.at[i, 'Destination'] = 'LIQUIDATE'     
                
    
    na_sn_df = na_sn_df.append(na_sn_df2, ignore_index=True)
    final_na_df = final_na_df.append(na_sn_df, ignore_index=True)
    
#final_na_df.to_excel('/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/allexcel_files/safetyNet_Liquidate_df.xlsx')

print("NA Safety Net and Liquidate | End Time: {}".format(datetime.now()))


#%%

Final_Df = Final_Df.append(final_na_df, ignore_index=True)
# In[37]:


Not_available_DF = ms[~ms['DISPOSITION'].isin(['READY TO DEPLOY', 'LAB', 'Not Decided'])]
not_avlbl_list = list(set(Not_available_DF['ATTItemNumber']))

#%%
print("Not available Safety Net and Liquidate | Start Time: {}".format(datetime.now()))

Not_available_DF['Model_Safety_Net'] = np.where(Not_available_DF.Model == 'N-A',0,
                    np.where(Not_available_DF.Model_Demand_Past_12_Month > Not_available_DF.Model_Demand_Future_12_Month,
                             3*Not_available_DF.Model_Demand_Past_12_Month, 3*Not_available_DF.Model_Demand_Future_12_Month))


final_not_avlbl_df = pd.DataFrame() 

for n in not_avlbl_list:
    not_avlbl_keep_qty = 0
    not_avlbl_sn_df2 = pd.DataFrame() 
    
    not_avlbl_sn_df = Not_available_DF[Not_available_DF["ATTItemNumber"]==n]
    not_avlbl_model_safety_net = np.mean(not_avlbl_sn_df['Model_Safety_Net'])  
        
    not_avlbl_keep_qty_data = len(keep_list.loc[keep_list['Item'] == n,'Keep Quantity'].values)
    
    if not_avlbl_keep_qty_data > 0:
        not_avlbl_keep_qty = keep_list.loc[keep_list['Item'] == n,'Keep Quantity'].values[0] 
        
        for i,data in not_avlbl_sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if int(not_avlbl_keep_qty) > 0 :
                    if not_avlbl_keep_qty >= data['QuantityOnhand']:
                        not_avlbl_keep_qty = not_avlbl_keep_qty - data['QuantityOnhand']
                        not_avlbl_sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                        not_avlbl_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                    else:
                        bal = data['QuantityOnhand'] - not_avlbl_keep_qty
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = not_avlbl_keep_qty
                        split1['Disposition_Final'] = 'KEEP'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        not_avlbl_keep_qty = 0
                        
                        split2 = dict(data)                    
                        
                        if not_avlbl_model_safety_net > 0: 
                            if bal <= not_avlbl_model_safety_net: 
                                split2['QuantityOnhand'] = bal
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                not_avlbl_model_safety_net = not_avlbl_model_safety_net - bal
                            else:
                                bal2 = bal - not_avlbl_model_safety_net
                                split2['QuantityOnhand'] = not_avlbl_model_safety_net
                                split2['Disposition_Final'] = 'SAFETY NET'
                                split2['Destination'] = 'ON HAND INVENTORY'
                                not_avlbl_model_safety_net = 0

                                split3 = dict(data)
                                split3['QuantityOnhand'] = bal2
                                split3['Disposition_Final'] = 'LIQUIDATE'
                                split3['Destination'] = 'LIQUIDATE'
                        
                        else:
                            split2['QuantityOnhand'] = bal 
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'
                        
                        try:
                            not_avlbl_sn_df=not_avlbl_sn_df.drop([i])
                            not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split1, ignore_index=True)
                            not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split2, ignore_index=True)
                            not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split3, ignore_index=True)
                        except:
                            pass                
                
                elif not_avlbl_model_safety_net > 0:
                    if not_avlbl_model_safety_net >= data['QuantityOnhand']:
                        not_avlbl_sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                        not_avlbl_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        not_avlbl_model_safety_net = not_avlbl_model_safety_net - data['QuantityOnhand']
                    else:
                        bal = data['QuantityOnhand'] - not_avlbl_model_safety_net
                        split1 = dict(data) 
                        split1['QuantityOnhand'] = not_avlbl_model_safety_net
                        split1['Disposition_Final'] = 'SAFETY NET'
                        split1['Destination'] = 'ON HAND INVENTORY'
                        not_avlbl_model_safety_net = 0 

                        split2 = dict(data)
                        split2['QuantityOnhand'] = bal
                        split2['Disposition_Final'] = 'LIQUIDATE'
                        split2['Destination'] = 'LIQUIDATE'

                        try:
                            not_avlbl_sn_df=not_avlbl_sn_df.drop([i])
                            not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split1, ignore_index=True)
                            not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split2, ignore_index=True)
                        except:
                            pass 

                else:
                    not_avlbl_sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                    not_avlbl_sn_df.at[i, 'Destination'] = 'LIQUIDATE' 
        
    else:    
        for i,data in not_avlbl_sn_df.iterrows():
            try:
                del(split1)
                del(split2)
                del(split3)
            except:
                pass

            if data['Disposition_Final'] == 'x' and data['Destination'] == 'y':
                if not data['ExternalDownloadFlag'] in(['B','X']):
                    not_avlbl_sn_df.at[i, 'Disposition_Final'] = 'NOT TO LIQUIDATE - Ext Dwld Flg'
                    not_avlbl_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                else: 
                    if int(not_avlbl_keep_qty) > 0 :
                        if not_avlbl_keep_qty >= data['QuantityOnhand']:
                            not_avlbl_keep_qty = not_avlbl_keep_qty - data['QuantityOnhand']
                            not_avlbl_sn_df.at[i, 'Disposition_Final'] = 'KEEP'
                            not_avlbl_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                        else:
                            bal = data['QuantityOnhand'] - not_avlbl_keep_qty
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = not_avlbl_keep_qty
                            split1['Disposition_Final'] = 'KEEP'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            not_avlbl_keep_qty = 0
                            
                            split2 = dict(data)
                            
                            if not_avlbl_model_safety_net > 0: 
                                if bal <= not_avlbl_model_safety_net: 
                                    split2['QuantityOnhand'] = bal
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    not_avlbl_model_safety_net = not_avlbl_model_safety_net - bal
                                else:
                                    bal2 = bal - not_avlbl_model_safety_net
                                    split2['QuantityOnhand'] = not_avlbl_model_safety_net
                                    split2['Disposition_Final'] = 'SAFETY NET'
                                    split2['Destination'] = 'ON HAND INVENTORY'
                                    not_avlbl_model_safety_net = 0

                                    split3 = dict(data)
                                    split3['QuantityOnhand'] = bal2
                                    split3['Disposition_Final'] = 'LIQUIDATE'
                                    split3['Destination'] = 'LIQUIDATE'
                            
                            else:
                                split2['QuantityOnhand'] = bal 
                                split2['Disposition_Final'] = 'LIQUIDATE'
                                split2['Destination'] = 'LIQUIDATE'
                            try:
                                not_avlbl_sn_df=not_avlbl_sn_df.drop([i])
                                not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split1, ignore_index=True)
                                not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split2, ignore_index=True)
                                not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split3, ignore_index=True)
                            except:
                                pass                    
                    
                    elif not_avlbl_model_safety_net > 0:
                        if not_avlbl_model_safety_net >= data['QuantityOnhand']:
                            not_avlbl_sn_df.at[i, 'Disposition_Final'] = 'SAFETY NET'
                            not_avlbl_sn_df.at[i, 'Destination'] = 'ON HAND INVENTORY'
                            not_avlbl_model_safety_net = not_avlbl_model_safety_net - data['QuantityOnhand']
                        else:
                            bal = data['QuantityOnhand'] - not_avlbl_model_safety_net
                            split1 = dict(data) 
                            split1['QuantityOnhand'] = not_avlbl_model_safety_net
                            split1['Disposition_Final'] = 'SAFETY NET'
                            split1['Destination'] = 'ON HAND INVENTORY'
                            not_avlbl_model_safety_net = 0 

                            split2 = dict(data)
                            split2['QuantityOnhand'] = bal
                            split2['Disposition_Final'] = 'LIQUIDATE'
                            split2['Destination'] = 'LIQUIDATE'

                            try:
                                not_avlbl_sn_df=not_avlbl_sn_df.drop([i])
                                not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split1, ignore_index=True)
                                not_avlbl_sn_df2 = not_avlbl_sn_df2.append(split2, ignore_index=True)
                            except:
                                pass 

                    else:
                        not_avlbl_sn_df.at[i, 'Disposition_Final'] = 'LIQUIDATE'
                        not_avlbl_sn_df.at[i, 'Destination'] = 'LIQUIDATE'     
                
    
    not_avlbl_sn_df = not_avlbl_sn_df.append(not_avlbl_sn_df2, ignore_index=True)
    final_not_avlbl_df = final_not_avlbl_df.append(not_avlbl_sn_df, ignore_index=True)
    
#final_na_df.to_excel('/home/shubhamrelekar/Documents/Xcaliber/XcaliberCodes/PythonScripts/disposition_scripts_JyuNb/allexcel_files/safetyNet_Liquidate_df.xlsx')

print("Not available Safety Net and Liquidate | End Time: {}".format(datetime.now()))


# In[39]:


Final_Df = Final_Df.append(final_not_avlbl_df, ignore_index=True)


# In[41]:


#np.sum(Final_Df['QuantityOnhand'])


# In[42]:


Final_Df.to_excel("C:/Users/UtkarshMishra/Desktop/Phoenix Innovations/final_Disposition_df_Jan_3rd_2022_including_integrated_2.xlsx")

    
#%%
