from googleads import adwords
import pandas as pd
import time
import logic
import queue
import utility
import threading
import logging
import re
import report_utility
import spreadsheet
import os

API_VERSION = utility.get_google_ads_api_version()
DB_NAME = "pausedRemovedkeywords"
SCRIPT_NAME = "pausedRemovedKeywords"
PRODUCTION_MODE = False
BASE_DIR = utility.get_credentials_folder_path()
credentials_path = utility.get_path_of_folder_in_dir(BASE_DIR,'CREDENTIALS')
MAIN_SPREADSHEET_ID = utility.get_execution_url_id(PRODUCTION_MODE)
all_clients=spreadsheet.get_accounts_data(credentials_path,
															SCRIPT_NAME,
															spreadsheet_id='1hoPoTuSvw_ZVpnA6RBxyYt3CSrdX1k0JU4sgYNvxWjE',
															sheet_name = 'Sheet1',
															required_customer_ids = [],
															client_only = True)

def main(client):
	customer_ids=list(all_clients.keys())
	# print(customer_ids)
	# return
	account_performance_data=[]
	
	start_time=time.time()
	# Entering the data in timestamp file.
	time_stamp_file_path = utility.get_path_of_timestamp_file(
													BASE_DIR, SCRIPT_NAME)
	#print(('Time stamp path : '+time_stamp_file_path))
	timestamp_file = open(time_stamp_file_path,"a+")
	current_time = time.asctime( time.localtime(time.time()) )
	timestamp_file.write(
					"\n*************************************************")
	timestamp_file.write("\n"+SCRIPT_NAME+" Script running started on "
						 +str(len(customer_ids)) +" accounts,start time: "
						 +current_time)
	timestamp_file.close()
	logic.main(client,customer_ids,time_stamp_file_path,API_VERSION,account_performance_data)
	

if __name__ == '__main__':
	adwords_client = adwords.AdWordsClient.LoadFromStorage(
							credentials_path+"googleads.yaml")
	main(adwords_client)
