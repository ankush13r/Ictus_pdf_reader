import extractPdfData
import sys

GENDER= {"male":["una paciente","mujer","femenino","fumadora",],"female":["varón","un paciente","el paciente","hombre","fumador"]}


def find_gender(data):
    lower_case_date = data.lower()
    key =""
    for key,value_list in GENDER.items():
        for value in value_list:
            pos = lower_case_date.find(value)
            if pos != -1:
                return value
    return None

<<<<<<< HEAD
def Anamnesis_info(Anamnesis):
    gender = find_gender(Anamnesis)
=======
PATTERN_FIND_INDICES = r".*[^\.](?=\.{5,})"
# Pattern for find indexes. In pdf all idexes finish with ...... minimum 6 point (ej: any index ...........)
# The patter will just look for all lines those have this format (any index .....),
# from those lines it will get all indices, but without any points (....)

PATTERN_FIND_SPACE_AFTER_INDEX = r"(?<=\.{6})\s(?=\w)"


PATTERN_FIND_PAGE_NUMBER = r"-\s\d+\s-"


PATTERN_FIND_WORD_SPLITED = r"- (?=\w)"

PATTERN_FIND_MANY_SPACE = " +|"+chr(160)+"+"
def get_pdf_data(file_root):

    
    pdf_file = open(file_root,"r") ###
    content = pdf_file.read()

#    pdf_file = open(file_root,"rb")
#    content = rPDF.readPDF(pdf_file)
    
    content_temp = re.sub(PATTERN_REPLACS_lINE_BREAK,' ',content)

    content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp)
    content_temp = re.sub(PATTERN_FIND_SPACE_AFTER_INDEX,"\n",content_temp)
    content_temp = re.sub(r" +",' ',content_temp)

    content_temp = re.sub(r"\(cid:\d*\)",'',content_temp)

    content_temp = re.sub(PATTERN_FIND_PAGE_NUMBER,'',content_temp)
    content_temp = re.sub(PATTERN_FIND_WORD_SPLITED,'',content_temp)
>>>>>>> 5cbc346ee369f642c5c4dcb7fcedc61e9872c778
    


    data_dict = {"gender":gender}
    print(gender)
    return gender

<<<<<<< HEAD

def extract_data_from_cases(dictionary):

    for key, paragraphs in dictionary.items():
        gender = Anamnesis_info(paragraphs[0])

        
=======
def get_indices_end_position(data):
    return data.find("Autores")
    
def get_indices_start_position(data):
    return data.find("Índice")

def get_indices(data):
 
    end_indices = get_indices_end_position(data)
    start_indices = get_indices_start_position(data)
    small_data = data[start_indices:end_indices] ### Devided data for getting indices, with this i get all data until last index.


    indices_iter = re.finditer(PATTERN_FIND_INDICES,small_data) #Iterable object that contain start, end position and also the matching string of each index
    indices_list = []
    i =1
    for index_pos in indices_iter:
        index_striped = (index_pos.group().strip()).upper()
        indices_list.append(index_striped)
        print(i,index_striped)
        i+=1
        
    return indices_list

def split_all_cases(data,indices,pattern):
    dictionary = dict()
    

    case_list = data.split(pattern)[1:]       
    print("Total clinical cases: ",len(case_list))
    print(len(indices))
    for index, case in zip(indices,case_list):
        dictionary[index] = case   
    return dictionary       
>>>>>>> 5cbc346ee369f642c5c4dcb7fcedc61e9872c778


<<<<<<< HEAD
=======
    data = get_pdf_data(file_root)
    indices = get_indices(data)

    list_of_all_cases = split_all_cases(data,indices,"CASO CLÍNICO")
>>>>>>> 5cbc346ee369f642c5c4dcb7fcedc61e9872c778

def main(arguments):       
    if not len(arguments) == 2:
        print("Expected 1 argument, but you are passing " + str(len(arguments)-1))
        return False
    file_root = arguments[1]
    dictionary = extractPdfData.create_cases_dict(file_root)
    extract_data_from_cases(dictionary)




<<<<<<< HEAD
=======
def main(arguments):
    if not len(arguments) == 2:
        print("Expected 1 argument, but you are passing " + str(len(arguments)-1))
    file_root = arguments[1]
    cases_dictionary = extract_all_cases(file_root)
    i = 0
    for key , value in cases_dictionary.items():
        i += 1
        file = open("data.txt","a+")
        file.write("--->"+str(i)+").  " +key+"\n" +"\n"+value)
        
>>>>>>> 5cbc346ee369f642c5c4dcb7fcedc61e9872c778
if __name__== "__main__":
      main(sys.argv)