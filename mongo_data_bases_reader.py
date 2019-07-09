
from pymongo import MongoClient
from pprint import pprint

import logging

#DEBUG ,INFO, WARNING, ERROR, CRITICAL
#----------------------------------------------------#
#----------------logging setting---------------------#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#Formatter handdler
console_formatter = logging.Formatter('%(levelname)s:%(name)s: <<%(message)s>>')
file_formatter = logging.Formatter('%(levelname)s:%(asctime)s: <<%(message)s>>')
#create Handlers
file_handler = logging.FileHandler('logTest.log')
console_handler = logging.StreamHandler()
#set Lever
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)
#set Formatter
file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)
#add Handler
logger.addHandler(file_handler)
logger.addHandler(console_handler)

#logger instead of logging
#---------------logging setting--------------------#

class Mongo:
    """
        Mongo: With this class you can get data from DATA BASES, 
        if you want to use it you must create Mongo class object, passing it same arguments.
        Arguments: (DATA_BASES_name, Table_name).
        And it will connect automatically with your local host: //localhost:27017/
        Example:
            object_name = Mongo(Data_bases_name, Table_name)
            object_name.method_name(arguments...)
        After all you'll be able to use all methods
    """

    """
        Methods: 
        By this all you'll get a cursor of data exiting in the table.
        And also it will print the number of rows found.

        Otherwise, it can't find, than you'll receive empty cursor 
        and also it will print <<no record found!>>.
                
    """
    def __init__(self, db_name, col_name):
        client = MongoClient('mongodb://localhost:27017/')
        db = client[db_name]
        self.collection = db[col_name]


    """
        get_all_data: This method return a cursor of all data exiting in the table.
        It recives two arguments but both are not required. If you want to sort you data, 
        you must pass arguments.
        Otherwise, it will be sorted randomly.
        example: 
            get_data_by_key(key_to_sortBy, value_to_sortBy)
            -> value_to_sortBY: Must be integer (1): ascending, (-1): descending 
    """
    def get_all_data(self,sort_key,sort_value):

        sort_key,sort_value = self.__valid_sort_key(sort_key,sort_value,"None")
        cursor = self.collection.find().sort(sort_key,sort_value)
        self.__cursor_len(cursor)
        return cursor


    """
        get_data_by_key: This method return a cursor of specific data found by condition.
        It receive two 4 arguments, 2 of them are required.
        example: 
            get_data_by_key(key, value, key_to_sortBy, value_to_sortBy)
            -> value_to_sortBY: Must be integer (1): ascending, (-1): descending
            
    """
    def get_data_by_key(self,key,value,sort_key=None,sort_value=1):

        sort_key,sort_value = self.__valid_sort_key(sort_key,sort_value,key)
        try:
            val_int = int(value)
            cursor = self.collection.find({key:val_int}).sort(sort_key,sort_value)
        except:
            regex = f".*{value}+"   # Using regex if user just give some words of string. If it match with any string it will give true
            cursor = self.collection.find({key:{"$regex":regex}}).sort(sort_key,sort_value)
        self.__cursor_len(cursor)
        return cursor

    """
        get_data_by_key: This method return a cursor of specific data found by condition.
        It receive two 5 arguments, 3 of them are required.
        arguments: 
            get_data_by_key(key, start_value, end_value, key_to_sortBy, value_to_sortBy)
                The field (key) type must be numeric, in the table. Otherwise it will return empty cursor
                
                start_value and end_value must be Integer.
                value_to_sortBY: Must be integer (1): ascending, (-1): descending     
    """

    def get_data_in_interval(self,key,value1,value2,sort_key=None,sort_value=1):
        try:
            start = int(value1)
            end = int(value2)           
        except:
            print("Values must be Integer!\n")
            return None
        sort_key,sort_value = self.__valid_sort_key(sort_key,sort_value,key)
        cursor = self.collection.find({key:{"$gte": start,"$lte": end}}).sort(sort_key,sort_value)
        self.__cursor_len(cursor)
        return cursor

    def __valid_sort_key(self,sort_key, sort_value,key):
        if not sort_key:
            sort_key = key
        else:
            try:
                sort_key = str(sort_key)
            except:
                pass
        try:
            sort_value = int(sort_value)
        except:
            print("Sort_value must be integer 1: ascending, -1: descending ") 

        return sort_key,sort_value

    def __cursor_len(self,cursor):
        if cursor.count() != 0:
            print("Records found: ",cursor.count())
        else:
            print("No record found!")


