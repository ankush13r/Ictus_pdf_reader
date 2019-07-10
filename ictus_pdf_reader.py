"""You must have installed pymongo, if you don't have, you can do by next command line (just for linux): 
$ python -m pip install pymongo
$ python -m pip install --upgrade pymongo
If you couldn't install by previous command line or are not using , 
than you figure it out here: https://api.mongodb.com/python/current/installation.html
After all must start mongo.
"""

from extractPdfData import Data_extract
import sys
import re
from pymongo import MongoClient
import logging
from constants import GENDER, PATTERN_FIND_AGE

#DEBUG ,INFO, WARNING, ERROR, CRITICAL
#----------------------------------------------------#
#----------------logging setting---------------------#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#Formatter handdler
console_formatter = logging.Formatter('%(levelname)s:%(name)s: << %(message)s >>')
file_formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s << %(message)s >>')
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

"""
    Class Data_extracted: This class is for saving all important data extracted from the clinical cases. 
        Attributes: title, hopital_name, doctor, supervision, patient_gender, patient_age
        Methods:
            1) __str__: This is a override methods that return a string of all attributes.
            2) get_dictionary: The method return all data as a object type dict.
"""
class Data_extracted:
    def __init__(self,title,hospital_name,doctor,supervision,patient_gender,patient_age):
        logger.info("Initializing the class called Data_extracted")
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


"""
    find_gender: This method find patient's gender by mapping a GENDER list created manually.
            
            Receive:    It receives a paragraph titled by Anamnesis
            Return:     If it finds the gender than returns the type of gender (Hombre or Mujer) as a string. 
                        Otherwise returns None.
"""
def find_gender(anamnesis):
    logger.info("Finding patient's age")
    lower_case_date = anamnesis.lower()
    key =""
    for key,value_list in GENDER.items():
        for value in value_list:
            pos = lower_case_date.find(value)
            if pos != -1:       #If any match found then it will return the key (Hombre or Mujer)
                return key
    return None

"""
    find_age: The method for finding patient's age. To find the age it uses regex (<<"(?<=de\s)?(\d\d)(\s?años|\smeses)">>),
              that already defined before in a constant variable.
              If it finds the pattern than it parse the string and get first two digits, must be numeric.               
        
    Receive:  It receives a paragraph titled by Anamnesis   
     Return:  If found the age than return Intger of 2 digits.
                    Otherwise returns None.
"""
def find_age(anamnesis):
    logger.info("Finding patient's gender")
    matched = re.search(PATTERN_FIND_AGE, anamnesis)
    if matched:
        try:
            age = int(matched.group()[:2])
            return age
        except ValueError:
            pass
    else:
        return None

""" 
    patient_info: This methods is just for call and get data from other methods, those  which receive Anamnesis paragraph.
                  After getting all data it will return all data.
        Receive:  It receives a paragraph titled by Anamnesis.
         Return:  All data as tuple collected from other methods.
"""
def patient_info(anamnesis):
    logger.info("Extrating all important data like age, gender,etc.")
    patient_gender = find_gender(anamnesis)
    patient_age = find_age(anamnesis)
    return patient_gender,patient_age

#-------------------------------------------------------------#
"""
    hospital_info:  This method extracts all information about hospital and doctors like docter name, supervisions and hospital name.
            Receive: It receives a string that contain all info related with hopital as before explained.
            Return:  It returns  hospital_name, doctor together supervision at the same time as tuple type object.
"""
def hospital_info(string_hopital_info):
    logger.info("Extrating information of hopital and doctors like hospital_name, doctor, supervision.")
    
    # Hospital name starts with complejo, Hospital or Fundación. 
    # So it will check three time if the previous one couldn't been found. 
    # If any is asserted than it will getout.
    hosp_name_start_pos = string_hopital_info.find("Complejo")
    hosp_name_end_pos = string_hopital_info.find("\nCASO CLÍNICO")
    
    if  hosp_name_start_pos == -1:
        hosp_name_start_pos = string_hopital_info.find("Hospital")
        if hosp_name_start_pos == -1:
            hosp_name_start_pos = string_hopital_info.find("Fundación")

    hospital_name = ""
    if hosp_name_start_pos == -1 :
        hospital_name = None
        hosp_name_start_pos = hosp_name_end_pos 
        # If there is no hopital name than start position will be same as end position. 
        # Because, doing this i'm saving docter name's end position as hosp_name_start_pos '', 
    else:
        hospital_name = string_hopital_info[hosp_name_start_pos:hosp_name_end_pos]
     # Getting all string before hopital_name_position_start. 
     # And saving it dividing by \n (line break). First line contains docter name and next one supervision's name , maybe more than one
    doctors_names = string_hopital_info[:hosp_name_start_pos].split("\n")
    doctor = doctors_names[0].strip() #First line saved as Doctor name
    
    if doctor == '':
        doctor = None
    if len(doctors_names) > 1:
        supervision = doctors_names[1].split(",") # Next line is save as supevision as array type object, if exists. Otherwise as None
    else :
        supervision = [None] 
    logger.info("Return all information like hospital_name, doctor and supervision.")
    return hospital_name, doctor, supervision

#--------------------------------------------------#
"""
    create_extracted_data_object_list: Method for creating object of all data extracted by calling other methods, 
            like hopital_info, patient_info,etc. After getting all data it creates a object of type (class) << Data_extracted >>
            passing arguments like title,hospital_name, doctor, supervision,patient_gender,patient_age, etc.
            All objects made by each class will be saved in a list and returned.
        receives:   Dictionary which cotain title as key and divided paragraphs as value.
        return:     A list of objects type (class) << Data_extracted >>.
"""
def create_extracted_data_object_list(dictionary):
    """ paragraphs information:
    key: title                              paragraphs[0]: hospital_info,              
    paragraphs[1]: Anamnesis,               paragraphs[2]: Exploración física,
    paragraphs[3]: Pruebas complementarias, paragraphs[4]: Diagnóstico,
    paragraphs[5]: Tratamiento,             paragraphs[6]: Evolución, 
    paragraphs[7]: DISCUSIÓN,               paragraphs[8]: BIBLIOGRAFÍA
    """
    list_extracted_data = []
    logger.info("Making a loop for going through each case and get extract all data by case.")
    i = 1
    for title, paragraphs in dictionary.items():
        logger.info(f"Case nº {i}")
        i += 1
        logger.info(f"Calling the method hospital_info")            
        hospital_name, doctor, supervision = hospital_info(paragraphs[0])
        logger.info(f"Calling the method patient_info")                  
        patient_gender,patient_age = patient_info(paragraphs[1])
        extracted_data = Data_extracted(title,hospital_name, doctor, supervision,patient_gender,patient_age)
        list_extracted_data.append(extracted_data)
    logger.info(f"Returning list of objects type Extracted_data")     
    return list_extracted_data

#-------------------------Mongo-------------------------#
"""
    save_data_in_mongo: Method for saving all extracted data into the MongoDB (Data Bases).
               receive: list of all objects type Extracted_data.
               re
"""

def save_data_in_mongo(list_data_extracted,file_root):
    found = re.search("\d{4}",file_root)
    if found != -1:
        col_name = "clinical_cases_"+found.group()
    else:
        col_name = "clinical_cases"
        
    client = MongoClient('mongodb://localhost:27017/')
    db_name = "Ictus_clinical_case"
    db = client[db_name]
    collection = db[col_name]
    for num, data in enumerate(list_data_extracted):
        dictionary = data.get_dictionary()
        if collection.find_one({"Título":data.title}):
            logger.warning(f"Already exits in the DATA BASES: (Title: {data.title})")
        else:
            collection.insert_one(dictionary)
            logger.info(f"Saved data into MongoDB. nº {num +1}")
    return True

#---------------------------------------------------------#
def main(arguments):
    logger.info(f"####---------------Commenced---------------####")                  
    
    if not len(arguments) == 2:
        logger.warning("Expected 1 argument, but given " + str(len(arguments)-1))
        logger.info("Example: ictus_pdf_reader.py file_root")
        return False
    file_root = arguments[1]

    pdf_file = open(file_root,"r") #Prueba desde el fichero del texto hay que borrar lo
    content = pdf_file.read() # También hay que borrar lo.

    logger.info(f"Going to the method readPDF() with file root") 
    #content = extractPdfData.readPDF(file_root)                 
    logger.info(f"Going to the method fix_up_content with contents")                  
    content_fixedUP = Data_extract.fix_up_content(content)
    logger.info(f"Going to the method split_all_cases with content_fixedUP")                  
    cases_list = Data_extract.split_all_cases(content_fixedUP)
    logger.info(f"Going to the method make_case_dict with cases_list divided (split) previously")                  
    cases_dictionary = Data_extract.make_case_dict(cases_list) #title are saved as key and other data as value.
    logger.info(f"Going to the method list_dict_cases_divided_in_paragraphs with cases_dictionary made previously")                  
    list_dict_cases_divided_in_paragraphs = Data_extract.split_cases_by_paragraphs(cases_dictionary)  
    logger.info(f"Going to the method create_extracted_data_object_list with list of dictionaries made previously")                  
    data_list = create_extracted_data_object_list(list_dict_cases_divided_in_paragraphs) # The object contain case information
    logger.info(f"Going to the method save_data_in_mongo with all data list of object type (class) Extraced_data")                     
    save_data_in_mongo(data_list,file_root)

if __name__== "__main__":
    
    main(sys.argv)