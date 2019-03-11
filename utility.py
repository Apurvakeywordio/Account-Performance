from datetime import datetime
from _datetime import timedelta

import json
import os
import sys
import time




def get_credentials_folder_path():
    get_files_from_system_path = True # If True then takes from system,
                                       # if false takes folder
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    if get_files_from_system_path:
        BASE_DIR = os.path.expanduser('~')
        # print(BASE_DIR)
    else:
        BASE_DIR = parent_dir
    return BASE_DIR

BASE_DIR = get_credentials_folder_path()

def get_path_of_timestamp_file(BASE_DIR, SCRIPT_NAME):
    folder_path_of_timestamp_files  = get_path_of_folder_in_dir(
                                            BASE_DIR,
                                            'Running status');
    if not os.path.exists(folder_path_of_timestamp_files):
        os.makedirs(folder_path_of_timestamp_files)
        print('directory created.')
    time_stamp_file_path = get_path_of_file(
                                folder_path_of_timestamp_files,
                                SCRIPT_NAME+' timestamp.txt');
    return time_stamp_file_path


def get_path_parent_main_dir(arguments):
    if os.name == 'nt':
        report_folder_path = arguments[0].split('\\');
        PATH = ''
        itr = 0;
        while(itr<(len(report_folder_path)-3)):
            if PATH != '':
                PATH = PATH+'\\\\'+report_folder_path[itr]
            else:
                PATH = report_folder_path[itr]

        itr = itr+1
    else:
        report_folder_path = arguments[0].split('/');
        PATH = ''
        itr = 1;
        while(itr<(len(report_folder_path)-3)):
            if PATH != '':
                PATH = PATH+'/'+report_folder_path[itr];
            else:
                PATH = '/'+report_folder_path[itr];
            itr = itr+1
        print(('path of current dir : '+PATH))
    return PATH


def get_path_of_folder_in_dir(path_of_current_dir,folder_name):
    if os.name == 'posix':
        file_path = path_of_current_dir+'/'+folder_name+'/';
        return file_path
    else:
        file_path = path_of_current_dir+'\\'+folder_name+'\\';
    return file_path


def get_path_of_file(folder_path,file_name):
    if os.name == 'posix':
        file_path = folder_path+'/'+file_name;
    else:
        file_path = folder_path+'\\\\'+file_name;
    return file_path


def get_execution_url_id(production_mode):
    # BASE_DIR = BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if production_mode:
        url_type = "PRODUCTION_URL_ID"
    else:
        url_type = "TESTING_URL_ID"
    final_path = get_path_of_folder_in_dir(BASE_DIR,'CREDENTIALS')
    global_variables = json.load(open(final_path+'global_variables.json'))
    if url_type in global_variables:
        url_id = global_variables[url_type]
        return global_variables[url_type]
    else:
        print('global variable not found')


def get_spreadsheet_id_from_url(spreadsheet_url):
    print(spreadsheet_url)
    splited_data = spreadsheet_url.split('/')
    # print(splited_data);
    count = 0;
    for element in splited_data:
        # print(str(element))
        count = count+1;
        # print(count)
        if str(element) == 'd':
            break;
        # print('Final count : '+str(count))
    spreadsheet_id = splited_data[count]
    print(('Spreadsheet id is : '+spreadsheet_id))
    return spreadsheet_id


def get_google_ads_api_version():
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    final_path = get_path_of_folder_in_dir(BASE_DIR,'CREDENTIALS')
    api_version = json.load(open(final_path+'global_variables.json'))
    return api_version["API_VERSION"]


def db_engine(DB_NAME):
    # BASE_DIR =os.path.dirname(os.path.abspath(__file__))
    final_path = get_path_of_folder_in_dir(BASE_DIR,'CREDENTIALS')
    DATABASE_CREDENTIALS_FILE = final_path+'db_credentials.json'
    with open(DATABASE_CREDENTIALS_FILE) as data_file:
        data = json.load(data_file)
        db_host = data['credentials']['host']
        db_user = data['credentials']['user']
        db_password  = data['credentials']['password']
        db_name = DB_NAME
#         db_port = data['credentials']['port']
        create_engine_stmt = ("mysql+mysqldb://{}:{}@{}/{}?charset=utf8")\
                              .format(db_user,db_password,db_host,db_name)
        engine = sqlalchemy.create_engine(create_engine_stmt)
        return engine


def db_start(DB_NAME):
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    final_path = get_path_of_folder_in_dir(BASE_DIR,'CREDENTIALS')
    data = json.load(open(final_path+'db_credentials.json'))

    db = pymysql.connect(host = data["credentials"]['host'], 
                         user = data["credentials"]['user'],
                         password = data["credentials"]['password'],
                         db = DB_NAME,
                         charset="utf8")
    cursor = db.cursor()
    return db, cursor


def date_format(date_min, date_max):
    past_date_min = datetime.now() - timedelta(days=date_min)
    past_date_min = str(past_date_min)[:10].replace("-", "")
    past_date_max = datetime.now() - timedelta(days=date_max)
    past_date_max = str(past_date_max)[:10].replace("-", "")
    final_date_range = past_date_min+", "+past_date_max
    # print(final_date_range)
    return past_date_min, past_date_max


def RSQ(item):
    try:
        item=item.replace("'", "\\'");
    except:
        pass
    return item
    print("Number of rows:",len(rows))


def write_status_in_file(time_stamp_file_path, customer_name, 
                         customers, status):
    timestamp_file = open(time_stamp_file_path,"a+")
    current_end_time = time.asctime( time.localtime(time.time()))
    line_to_write = ("\n{} : {} : {} : {}").format(customer_name, customers, 
                                                   current_end_time, status)
    timestamp_file.write(line_to_write)
    timestamp_file.close()


def print_name_of_current_database(final_path):
    db, cursor = db_start()
    data = json.load(open(final_path+'db_credentials.json'))
    sql1=("USE {};").format(data['credentials']['db'])
    cursor.execute(sql1)
    sql2="SELECT DATABASE() FROM DUAL;"
    cursor.execute(sql2)
    for row in cursor.fetchall():
        database_name = str(row[0]);
        print(("Active database : {}".format(database_name)))
    update_charset_query = ("ALTER DATABASE {} CHARACTER SET \
                             utf8 COLLATE utf8_general_ci"\
                            .format(database_name))
    cursor.execute(update_charset_query)
    db.commit()
    db.close()


def drop_all_tables_in_database(DB_NAME):
    db, cursor = db_start(DB_NAME)
    sql = "SELECT table_name FROM information_schema.tables \
           WHERE table_schema='{}';".format(DB_NAME)
    cursor.execute(sql)
    for row in cursor.fetchall():
        query = "DROP TABLE "+row[0]
        cursor.execute(query)
    db.commit()
    print('all tables are removed from database...');





if __name__ == '__main__':
    drop_all_tables_in_database(DB_NAME='keywords_db')

