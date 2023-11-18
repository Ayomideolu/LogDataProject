import os
from datetime import datetime
#import re
import pandas as pd
from sqlalchemy import create_engine
import ast # Abstract syntax tree used for obtaining actual python objects from string
from dotenv import dotenv_values
dotenv_values()
from util import get_database_conn


###  Data Extraction layer
def extract_data():
    log_extract_data = []
    # DeclareS the json's dictionary confirmed 12 keys for locating values
    log_keys = ["event_date", "event_timestamp", "event_name", "event_params", "event_server_timestamp_offset", "user_pseudo_id", "user_properties", "user_first_touch_timestamp", "mobile_os_hardware_model", "language", "time_zone_offset_seconds", "version"]
    with open('logs/bq-logs-data.json', 'r') as log_file:
        for log_data in log_file:
            log_data = ast.literal_eval(log_data) # use for converting string to valid dict/lis/tuple etc
            log_date = log_data[log_keys[0]]
            event_date = datetime.strptime(log_date, '%Y%m%d')
            user_id = log_data[log_keys[5]]
            event_name = log_data[log_keys[2]]
            mobile_os_hardware_model = log_data[log_keys[8]]
            version = log_data[log_keys[11]]
            log_extract_data.append([event_date, user_id, event_name, mobile_os_hardware_model, version])
    #Copy extracted data to a pandas dataframe
    log_data = pd.DataFrame(log_extract_data, columns=['date', 'user_id', 'event_name', 'mobile_os_type', 'version'])
    # Export data to a CSV file. This is your stanging area
    filename = f'log_data_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
    path = f'raw/{filename}'
    if os.path.exists('raw') == False:
        os.mkdir('raw')
        log_data.to_csv(path, index= False) 
        print('Data extracted and written to file')
    else:
        log_data.to_csv(path, index= False)
        print('Data extracted and written to file')
