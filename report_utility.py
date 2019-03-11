import googleads.adwords
import googleads.errors
from datetime import timedelta
import time
import copy
import re
import utility
import pandas as pd
import multiprocessing
from queue import Empty
import xml.etree.ElementTree as ET
import spreadsheet
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
from _datetime import timedelta


# For calculation purpose
MILLION = 1000000
# No. of Days
DAYS = 7  
#No. Of Days in Year
NO_OF_DAYS=365
#No. Of Days in Month
NO_OF_DAYS_MONTH=30
     
def fetch_accountPerformance_weekly_report(client, customer_id, API_VERSION,account_performance_data):
    start_list=[]
    end_list=[]
    start_date_one,end_date_one=utility.date_format(DAYS,1)
    start_date_one = datetime.datetime.strptime(start_date_one,"%Y%m%d")
    end_date_one = datetime.datetime.strptime(end_date_one,"%Y%m%d")
    end_date_two=start_date_one+timedelta(days=-1)
    start_date_two=end_date_two+timedelta(days=-6)
    start_date_one=start_date_one.strftime('%Y%m%d')
    # start_date.append(start_date_one)
    start_date_two=start_date_two.strftime('%Y%m%d')
    # start_date.append(start_date_two)
    end_date_one=end_date_one.strftime('%Y%m%d')
    # end_date.append(end_date_one)
    end_date_two=end_date_two.strftime('%Y%m%d')
    # end_date.append(end_date_two)
    # print(list(zip(start_date,end_date)))
    # return

    start_list.append(start_date_one)
    start_list.append(start_date_two)
    end_list.append(end_date_one)
    end_list.append(end_date_two)
    for start_dates, end_dates in zip(start_list,end_list):
        # print(start_dates,end_dates)
        # print(type(start_dates),type(end_dates))

        # print(customer_id,start_dates,end_dates)
        report_downloader = client.GetReportDownloader(version=API_VERSION)
        # Create report definition.
        report = {
            'reportName': 'ACCOUNT_PERFORMANCE_REPORT',
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'ACCOUNT_PERFORMANCE_REPORT',
            'downloadFormat': 'XML',
            'selector': {
            'dateRange':{'min':start_dates,'max':end_dates},
            'fields': ['AccountDescriptiveName','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ValuePerConversion','ConversionRate']
            }
        }
        # Print out the report as a string

        data = report_downloader.DownloadReportAsString(report, 
                                                    skip_report_header=False, 
                                                    skip_column_header=False, 
                                                    skip_report_summary=False,
                                                    include_zero_impressions=True,
                                                    client_customer_id = customer_id)
        root=ET.fromstring(str(data))
        d={}
                
        for row in root.find("table").findall("row"):
                    
            d = row.attrib
            name=d['account']
            click=float(d['clicks'])
            impr=float(d['impressions'])
            ctr=float(d['ctr'].strip("%"))
            avgcpc=float(d['avgCPC'])
            cost=float(d['cost'])/MILLION
            conv=float(d['conversions'])
            cpcon=float(d['costConv'])/MILLION
            cvalue=float(d['totalConvValue'])

            if cost > 0:
                convpcost = float(cvalue)/cost
            else:
                convpcost=0
            convpcost= round(convpcost, 2)
                
            vpcon=float(d['valueConv'])
            rate=float(d['convRate'].strip("%"))
            account_performance_data.append([name,customer_id,click,impr,ctr,avgcpc,cost,conv,cpcon,cvalue,convpcost,vpcon,rate])

    
    
   
        
        # print(account_performance_data)
        # print(len(account_performance_data))
            
def fetch_accountPerformance_last_month_report(client, customer_id, API_VERSION,account_performance_data):
    start_list=[]
    end_list=[]
    start_date_one,end_date_one=utility.date_format(NO_OF_DAYS_MONTH,1)
    start_date_one = datetime.datetime.strptime(start_date_one,"%Y%m%d")
    end_date_one = datetime.datetime.strptime(end_date_one,"%Y%m%d")
    end_date_two=start_date_one+timedelta(days=-1)
    start_date_two=end_date_two+timedelta(days=-29)
    start_date_one=start_date_one.strftime('%Y%m%d')
    # start_date.append(start_date_one)
    start_date_two=start_date_two.strftime('%Y%m%d')
    # start_date.append(start_date_two)
    end_date_one=end_date_one.strftime('%Y%m%d')
    # end_date.append(end_date_one)
    end_date_two=end_date_two.strftime('%Y%m%d')
    # end_date.append(end_date_two)
    # print(list(zip(start_date,end_date)))
    # return

    start_list.append(start_date_one)
    start_list.append(start_date_two)
    end_list.append(end_date_one)
    end_list.append(end_date_two)
    for start_dates, end_dates in zip(start_list,end_list):
        # print(start_dates,end_dates)
        # return
        # start_date, end_date = utility.date_format(DAYS,1)
        report_downloader = client.GetReportDownloader(version=API_VERSION)
        # Create report definition.
        report = {
            'reportName': 'ACCOUNT_PERFORMANCE_REPORT',
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'ACCOUNT_PERFORMANCE_REPORT',
            'downloadFormat': 'XML',
            'selector': {
            'dateRange':{'min':start_dates,'max':end_dates},
            'fields': ['AccountDescriptiveName','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ValuePerConversion','ConversionRate'],
        

            }
        }
        # Print out the report as a string
        # print('downloading KEYWORDS_PERFORMANCE_REPORT')
        data = report_downloader.DownloadReportAsString(
                                    report, skip_report_header=False, 
                                    skip_column_header=False, 
                                    skip_report_summary=False,
                                    include_zero_impressions=True,
                                    client_customer_id = customer_id)
        root = ET.fromstring(str(data))
        # print('data downloaded')
        d={}
        for row in root.find("table").findall("row"):
            d = row.attrib
            name=d['account']
            click=float(d['clicks'])
            impr=float(d['impressions'])
            ctr=float(d['ctr'].strip("%"))
            avgcpc=float(d['avgCPC'])
            cost=float(d['cost'])/MILLION
            conv=float(d['conversions'])
            cpcon=float(d['costConv'])/MILLION
            cvalue=float(d['totalConvValue'])

            if cost > 0:
                convpcost = float(cvalue)/cost
            else:
                convpcost=0
            convpcost= round(convpcost, 2)
                    
            vpcon=float(d['valueConv'])
            rate=float(d['convRate'].strip("%"))
            account_performance_data.append([name,customer_id,click,impr,ctr,avgcpc,cost,conv,cpcon,cvalue,convpcost,vpcon,rate])

# def fetch_accountPerformance_current_month_report(client, customer_id, API_VERSION,account_performance_data):

     
  
#     # start_date, end_date = utility.date_format(DAYS,1)
#     report_downloader = client.GetReportDownloader(version=API_VERSION)
#     # Create report definition.
#     report = {
#         'reportName': 'ACCOUNT_PERFORMANCE_REPORT',
#         'dateRangeType': 'THIS_MONTH',
#         'reportType': 'ACCOUNT_PERFORMANCE_REPORT',
#         'downloadFormat': 'XML',
#         'selector': {
       
#         'fields': ['AccountDescriptiveName','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ValuePerConversion','ConversionRate'],
       

#         }
#     }
#     # Print out the report as a string
#     # print('downloading KEYWORDS_PERFORMANCE_REPORT')
#     data = report_downloader.DownloadReportAsString(
#                                 report, skip_report_header=False, 
#                                 skip_column_header=False, 
#                                 skip_report_summary=False,
#                                 include_zero_impressions=True,
#                                 client_customer_id = customer_id)
#     root = ET.fromstring(str(data))
#     # print('data downloaded')
#     d={}
#     for row in root.find("table").findall("row"):
#         d = row.attrib
#         name=d['account']
#         click=float(d['clicks'])
#         impr=float(d['impressions'])
#         ctr=float(d['ctr'].strip("%"))
#         avgcpc=float(d['avgCPC'])
#         cost=float(d['cost'])/MILLION
#         conv=float(d['conversions'])
#         cpcon=float(d['costConv'])/MILLION
#         cvalue=float(d['totalConvValue'])

#         if cost > 0:
#             convpcost = float(cvalue)/cost
#         else:
#             convpcost=0
#         convpcost= round(convpcost, 2)
                
#         vpcon=float(d['valueConv'])
#         rate=float(d['convRate'].strip("%"))
#         account_performance_data.append([name,customer_id,click,impr,ctr,avgcpc,cost,conv,cpcon,cvalue,convpcost,vpcon,rate])

       

def fetch_accountPerformance_yearly_report(client, customer_id, API_VERSION, account_performance_data):
    
    start_list=[]
    end_list=[]
    start_date_one,end_date_one=utility.date_format(NO_OF_DAYS,1)
    start_date_one = datetime.datetime.strptime(start_date_one,"%Y%m%d")
    end_date_one = datetime.datetime.strptime(end_date_one,"%Y%m%d")
    end_date_two=start_date_one+timedelta(days=-1)
    start_date_two=end_date_two+timedelta(days=-364)
    start_date_one=start_date_one.strftime('%Y%m%d')
    # start_date.append(start_date_one)
    start_date_two=start_date_two.strftime('%Y%m%d')
    # start_date.append(start_date_two)
    end_date_one=end_date_one.strftime('%Y%m%d')
    # end_date.append(end_date_one)
    end_date_two=end_date_two.strftime('%Y%m%d')
    # end_date.append(end_date_two)
    # print(list(zip(start_date,end_date)))
    # return

    start_list.append(start_date_one)
    start_list.append(start_date_two)
    end_list.append(end_date_one)
    end_list.append(end_date_two)
    # print(start_list,end_list)
    # return
    for start_dates, end_dates in zip(start_list,end_list):
        report_downloader = client.GetReportDownloader(version=API_VERSION)
        # Create report definition.
        report = {
            'reportName': 'ACCOUNT_PERFORMANCE_REPORT',
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'ACCOUNT_PERFORMANCE_REPORT',
            'downloadFormat': 'XML',
            'selector': {
            'dateRange':{'min':start_dates,'max':end_dates},
            'fields': ['AccountDescriptiveName','Clicks','Impressions','Ctr','AverageCpc','Cost','Conversions','CostPerConversion','ConversionValue','ValuePerConversion','ConversionRate'],
            

            }
        }
        # Print out the report as a string
        # print('downloading KEYWORDS_PERFORMANCE_REPORT')
        data = report_downloader.DownloadReportAsString(
                                    report, skip_report_header=False, 
                                    skip_column_header=False, 
                                    skip_report_summary=False,
                                    include_zero_impressions=True,
                                    client_customer_id = customer_id)
        root = ET.fromstring(str(data))
        # print('data downloaded')
        d={}
        for row in root.find("table").findall("row"):
            d = row.attrib
            name=d['account']
            click=float(d['clicks'])
            impr=float(d['impressions'])
            ctr=float(d['ctr'].strip("%"))
            avgcpc=float(d['avgCPC'])
            cost=float(d['cost'])/MILLION
            conv=float(d['conversions'])
            cpcon=float(d['costConv'])/MILLION
            cvalue=float(d['totalConvValue'])

            if cost > 0:
                convpcost = float(cvalue)/cost
            else:
                convpcost=0
            convpcost= round(convpcost, 2)
                    
            vpcon=float(d['valueConv'])
            rate=float(d['convRate'].strip("%"))
            account_performance_data.append([name,customer_id,click,impr,ctr,avgcpc,cost,conv,cpcon,cvalue,convpcost,vpcon,rate])
