"""You must have installed pymongo, if you don't have, you can do by next command line (only linux): 
$ python -m pip install pymongo
$ python -m pip install --upgrade pymongo
If you couldn't install by previous command line, 
than you figure it out here: https://api.mongodb.com/python/current/installation.html
"""

from extractPdfData import Data_extract
import sys
import re
from pymongo import MongoClient




GENDER= {"Hombre":["una paciente","mujer","femenino","fumadora",],"Mujer":["varón","un paciente","el paciente","hombre","fumador"]}
PATTERN_FIND_AGE = r"(?<=de\s)?(\d\d)(\s?años|\smeses)"

class Data_extracted:
    def __init__(self,title,hospital_name,doctor,supervision,patient_gender,patient_age):
        self.title = title
        self.hospital_name = hospital_name
        self.doctor = doctor
        self.supervision = supervision
        self.patient_gender = patient_gender
        self.patient_age = patient_age

    def __str__(self):
        if not None in self.supervision:
            tmp_supervision = ", ".join(self.supervision)
        else:
            tmp_supervision = "None"
        return str(f"Hospital: {self.hospital_name},\tMédico: {self.doctor},\tSupervision: {tmp_supervision}\t"+
            f"Género_paciente: {self.patient_gender},\tEdad_paciente: {self.patient_age}")

    def get_dictionary(self):
        return dict({"Título":self.title, "Hospital":self.hospital_name, "Médico": self.doctor, "Supervision": self.supervision,
        "Género_paciente":self.patient_gender, "Edad_paciente": self.patient_age})

##########################################################

def find_gender(anamnesis):
    lower_case_date = anamnesis.lower()
    key =""
    for key,value_list in GENDER.items():
        for value in value_list:
            pos = lower_case_date.find(value)
            if pos != -1:       #If any match found then it will return the key (Hombre or Mujer)
                return key
    return None

def find_age(anamnesis):
    matched = re.search(PATTERN_FIND_AGE, anamnesis)
    if matched:
        return matched.group()
    else:
        return None

def patient_info(anamnesis):

    patient_gender = find_gender(anamnesis)
    patient_age = find_age(anamnesis)
    return patient_gender,patient_age


#-------------------------------------------------------------#

def hospital_info(string_hopital_info):
    hosp_name_end_pos = string_hopital_info.find("\nCASO CLÍNICO")
    hosp_name_start_pos = string_hopital_info.find("Complejo")
    if  hosp_name_start_pos == -1:
        hosp_name_start_pos = string_hopital_info.find("Hospital")
        if hosp_name_start_pos == -1:
            hosp_name_start_pos = string_hopital_info.find("Fundación")

    hospital_name = string_hopital_info[hosp_name_start_pos:hosp_name_end_pos]
    if hosp_name_start_pos == -1 :
        hospital_name = None
        hosp_name_start_pos = hosp_name_end_pos
    doctors_names = string_hopital_info[:hosp_name_start_pos].split("\n")
    doctor = doctors_names[0].strip()
    
    if doctor == '':
        doctor = None
    if len(doctors_names) > 1:
        supervision = doctors_names[1].split(",")
    else :
        supervision = [None]

    return hospital_name, doctor, supervision

#--------------------------------------------------#

def create_extracted_data_object_list(dictionary):
    """ paragraphs information:
    key: title                              paragraphs[0]: hospital_info,              
    paragraphs[1]: Anamnesis,               paragraphs[2]: Exploración física,
    paragraphs[3]: Pruebas complementarias, paragraphs[4]: Diagnóstico,
    paragraphs[5]: Tratamiento,             paragraphs[6]: Evolución, 
    paragraphs[7]: DISCUSIÓN,               paragraphs[8]: BIBLIOGRAFÍA 
    """
    list_extracted_data = []
    for title, paragraphs in dictionary.items():        
        hospital_name, doctor, supervision = hospital_info(paragraphs[0])
        patient_gender,patient_age = patient_info(paragraphs[1])

        extracted_data = Data_extracted(title,hospital_name, doctor, supervision,patient_gender,patient_age)
        list_extracted_data.append(extracted_data)

    return list_extracted_data


#-------------------------Mongo-------------------------#
def save_data_in_mongo(list_data_extracted,file_root):

    client = MongoClient('mongodb://localhost:27017/')
    db = client["Ictus_clinical_case"]
    collection = db.Clinical_cases
    for data in list_data_extracted:
        dictionary = data.get_dictionary()
        if collection.find_one({"Título":dictionary.title}):
            print(exite)

        collection.insert_one(dictionary)
    print("Saved")




#---------------------------------------------------------#
def main(arguments):       
    if not len(arguments) == 2:
        print("Expected 1 argument, but given " + str(len(arguments)-1))
        return False
    file_root = arguments[1]

    #pdf_file = open(file_root,"rb")
    #content = Data_extract.readPDF(pdf_file)

    pdf_file = open(file_root,"r") #Prueba desde el fichero del texto
    content = pdf_file.read()
    content_fixedUP = Data_extract.fix_up_content(content)
    cases_list = Data_extract.split_all_cases(content_fixedUP)
    cases_dictionary = Data_extract.make_case_dict(cases_list) #title as key and other data as value
    list_dict_cases_devided_in_paragraphs = Data_extract.split_cases_by_paragraphs(cases_dictionary)
    
    data_list = create_extracted_data_object_list(list_dict_cases_devided_in_paragraphs) # The object contain case information
    save_data_in_mongo(data_list,file_root)




if __name__== "__main__":
      main(sys.argv)