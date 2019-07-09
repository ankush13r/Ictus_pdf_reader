
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')

dbAdmin = client.admin

serverStatus = dbAdmin.command("serverStatus")

pprint(serverStatus)