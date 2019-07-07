import extractPdfData
import sys
import re

GENDER= {"Hombre":["una paciente","mujer","femenino","fumadora",],"Mujer":["varón","un paciente","el paciente","hombre","fumador"]}

PATTERN_FIND_AGE = r"(?<=de\s)?(\d\d)(\s?años|\smeses)"

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

def anamnesis_info(anamnesis):

    gender = find_gender(anamnesis)
    age = find_age(anamnesis)
    data_dict = {"Genero":gender,"Edad":age}
    return data_dict

def hospital_info(string):
    hosp_name_end_pos = string.find("\nCASO CLÍNICO")
    hosp_name_start_pos = string.find("Complejo")
    if  hosp_name_start_pos == -1:
        hosp_name_start_pos = string.find("Hospital")
        if hosp_name_start_pos == -1:
            hosp_name_start_pos = string.find("Fundación")
 
    hospital_name = string[hosp_name_start_pos:hosp_name_end_pos]
    if hosp_name_start_pos == -1 :
        hospital_name = None
        hosp_name_start_pos = hosp_name_end_pos
        input()

    doctors_names = string[:hosp_name_start_pos].split("\n")
    doctor = doctors_names[0].strip()
    
    if doctor == '':
        doctor = None
    if len(doctors_names) > 1:
        supervision = doctors_names[1].split(",")
    else :
        supervision = [None]
    
    dictionary = {"Nombre_hopital": hospital_name,"Doctor":doctor,"Supervision": supervision}
    print(dictionary)
    return dictionary


def extract_data_from_cases(dictionary):
    for key, paragraphs in dictionary.items():
        title = key         #The title is saved as key.
        hospital_data = hospital_info(paragraphs[0])
        anamnesis_data = anamnesis_info(paragraphs[1]) 


def main(arguments):       
    if not len(arguments) == 2:
        print("Expected 1 argument, but you are passing " + str(len(arguments)-1))
        return False
    file_root = arguments[1]
    dictionary = extractPdfData.create_cases_dict(file_root)
    extract_data_from_cases(dictionary)


if __name__== "__main__":
      main(sys.argv)