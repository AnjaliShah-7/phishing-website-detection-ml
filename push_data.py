import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from Phishing.exception.exception import PhishingException
from Phishing.logging.logger import logging

class PhishingDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise PhishingException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise PhishingException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise PhishingException(e,sys)
        
if __name__=='__main__':
    FILE_PATH="Phishing_data\phishing.csv"
    DATABASE="PhishingDB"
    Collection="PhishingData"
    phishing_obj=PhishingDataExtract()
    records=phishing_obj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records= phishing_obj.insert_data_mongodb(records,DATABASE,Collection)
    #logging.info(f"{no_of_records} records inserted successfully.")
    print(f"{no_of_records} records inserted successfully into MongoDB.")
        


    
    
