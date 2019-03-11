import googleads.adwords
import googleads.errors
import report_utility
import time
import logging
import utility
import pandas as pd
import multiprocessing
from queue import Empty
import spreadsheet
import threading
from datetime import date, time
import os 
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


def main(client,customer_ids,time_stamp_file_path,API_VERSION,account_performance_data):
    fetch_accountPerformance_report_current_week(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data)
	
    # fetch_accountPerformance_previous_month_report(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data)
    # fetch_accountPerformance_current_month_report(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data)
    
    fetch_accountPerformance_yearly_report(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data)

def fetch_accountPerformance_report_current_week(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data):         
    threads = []
    for customer_id in customer_ids:
        t = threading.Thread(
                        target=report_utility.fetch_accountPerformance_weekly_report,
                        args=(client, customer_id, API_VERSION,account_performance_data))
                                
        threads.append(t)
        # print('starting thread for customer_id = ',customer_id)
        t.start()
    for t in threads:
        t.join()
    #print("Length of the thread is:",len(threads))
    #print(account_performance_data)
    account_performnace_dataframe = pd.DataFrame(account_performance_data,index=None,columns=['Name','customer_id','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ConveValuePcost','ValuePerConversion','ConversionRate'])
    writer = ExcelWriter('Account2.xlsx')
    account_performnace_dataframe.to_excel(writer,'Clicks',index=False)
    writer.save()


    
   
def get_click_performance():
    xls=pd.ExcelFile("Account.xlsx")
   
    df1=pd.read_excel(xls, 'Sheet1')
    df2=pd.read_excel(xls, 'Sheet2')
    listOfNames=df1["Name"].tolist()
    df2=df2.loc[48:,["Name","Clicks"]]
    previous_click_list=df2['Clicks'].tolist()
    df1=df1.loc[:,["Name","Clicks"]]
    latest_click_list=df1['Clicks'].tolist()
    
    # print(len(latest_click_list))
    # print(len(previous_click_list))
    

    new_data=pd.DataFrame({
        'Name':listOfNames,
        'Latest Clicks':latest_click_list,
        'Previous Clicks': previous_click_list,

    })
    writer = ExcelWriter('FinalPerformance.xlsx')
    new_data.to_excel(writer,'Click_Performance')
    writer.save()
    
    
def fetch_accountPerformance_previous_month_report(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data):
    threads = []
    for customer_id in customer_ids:
        t = threading.Thread(
                        target=report_utility.fetch_accountPerformance_last_month_report,
                        args=(client, customer_id, API_VERSION,account_performance_data))
                                
        threads.append(t)
        # print('starting thread for customer_id = ',customer_id)
        t.start()
    for t in threads:
        t.join()
    #print("Length of the thread is:",len(threads))
    #print(account_performance_data)
    account_performance_dataframe = pd.DataFrame(account_performance_data,index=None,columns=['Name','customer_id','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ConveValuePcost','ValuePerConversion','ConversionRate'])
    writer = ExcelWriter('Month.xlsx')
    account_performance_dataframe.to_excel(writer,'sheet1',index=False)
    writer.save()   
    

def fetch_accountPerformance_current_month_report(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data):
    threads = []
    for customer_id in customer_ids:
        t = threading.Thread(
                        target=report_utility.fetch_accountPerformance_current_month_report,
                        args=(client, customer_id, API_VERSION,account_performance_data))
                                
        threads.append(t)
        # print('starting thread for customer_id = ',customer_id)
        t.start()
    for t in threads:
        t.join()
    #print("Length of the thread is:",len(threads))
    #print(account_performance_data)
    monthly_dataframe = pd.DataFrame(account_performance_data,index=None,columns=['Name','customer_id','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ConveValuePcost','ValuePerConversion','ConversionRate'])
    writer = ExcelWriter('firstMonth.xlsx')
    account_performance_data.to_excel(writer,'sheet1',index=False)
    writer.save() 

def fetch_accountPerformance_yearly_report(client, customer_ids,time_stamp_file_path,API_VERSION,account_performance_data):
    threads = []
    for customer_id in customer_ids:
        t = threading.Thread(
                        target=report_utility.fetch_accountPerformance_yearly_report,
                        args=(client, customer_id, API_VERSION, account_performance_data))
                                
        threads.append(t)
        # print('starting thread for customer_id = ',customer_id)
        t.start()
    for t in threads:
        t.join()
    #print("Length of the thread is:",len(threads))
    #print(account_performance_data)
    monthly_dataframe = pd.DataFrame(account_performance_data,index=None,columns=['Name','customer_id','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ConveValuePcost','ValuePerConversion','ConversionRate'])
    writer = ExcelWriter('Year.xlsx')
    monthly_dataframe.to_excel(writer,'sheet1',index=False)
    writer.save() 

    
   