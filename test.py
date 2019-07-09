from mongo_data_bases_reader import Mongo
from pprint import pprint

mongo = Mongo("Ictus_clinical_case","clinical_cases_2015")

#datas = mongo.get_all_data()
datas = mongo.get_data_in_interval("Edad_paciente","30","39","Edad_paciente",-1)

for data in datas:
    pprint(data)
    print()



