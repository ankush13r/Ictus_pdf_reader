from io import open 
import re
import pdf_reader as rPDF
import pdf_to_text
import sys


PATTERN_REPLACS_lINE_BREAK =r"((?<=[^.\n])\n)|\x0c"  
# Pattern for replace a single {line break} by a {space} because all pdf conten all data in {table format},
# So, if there is single line break it will findout, which we need to replace by a space.


<<<<<<< HEAD
PATTERN_FIND_CASE_START_PAGE = r".*[^\.](?=\.{6,})"
=======
PATTERN_FIND_INDICES = r".*[^\.](?=\.{6,})"
>>>>>>> 5cbc346ee369f642c5c4dcb7fcedc61e9872c778
# Pattern for find indexes. In pdf all idexes finish with ...... minimum 6 point (ej: any index ...........)
# The patter will just look for all lines those have this format (any index .....),
# from those lines it will get all indices, but without any points (....)

PATTERN_FIND_SPACE_AFTER_INDEX = r"(?<=\.{6})\s(?=\w)"
<<<<<<< HEAD
PATTERN_FIND_PAGE_NUMBER = r"-\s\d+\s-"
PATTERN_FIND_WORD_SPLITED = r"- (?=\w)"
PATTERN_FIND_MANY_SPACE = r" +|"+chr(160)+"+"
PATTERN_RARE_CARACTERS = r"\(cid:\d*\)"
PATTERN_FIND_HEADER = r".*CONCURSO DE CASOS CLÍNICOS.*20\d\d"

case_paragraphs = ("Anamnesis","Exploración física","Pruebas complementarias","Diagnóstico","Tratamiento","Evolución", "DISCUSIÓN","BIBLIOGRAFÍA","Figura 1.")



def get_pdf_data(file_root):

    
    pdf_file = open(file_root,"r") ###
    content = pdf_file.read()

    #pdf_file = open(file_root,"rb")
    #content = rPDF.readPDF(pdf_file)
    

    content_temp = re.sub(PATTERN_REPLACS_lINE_BREAK,' ',content) #Replace line break by a space.
    content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp) #Strip all spaces those are repeated.
    content_temp = re.sub(PATTERN_FIND_SPACE_AFTER_INDEX,"\n",content_temp) #
    content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp) #Strip all spaces those are repeated, again
    content_temp = re.sub(PATTERN_RARE_CARACTERS,'',content_temp) # Deleting all rare caracter as  (cid:32)
    content_temp = re.sub(PATTERN_FIND_PAGE_NUMBER,'',content_temp)
    content_temp = re.sub(PATTERN_FIND_HEADER,'',content_temp)


    final_content = re.sub(PATTERN_FIND_WORD_SPLITED,'',content_temp)

    return final_content
  


def split_all_cases(data):
    list = data.split("Supervisión:")   
    print("Total number of clinical cases: ", len(list)-2)
    return list      

=======


PATTERN_FIND_PAGE_NUMBER = r"-\s\d+\s-"


PATTERN_FIND_WORD_SPLITED = r"- (?=\w)"

PATTERN_FIND_MANY_SPACE = " +|"+chr(160)+"+"
def get_pdf_data(file_root):

    
    #pdf_file = open(file_root,"r") ###
    #content = pdf_file.read()

    pdf_file = open(file_root,"rb")
    content = rPDF.readPDF(pdf_file)
    
    output_file = open("result2016.txt","w")
    output_file.write(content)

    content_temp = re.sub(PATTERN_REPLACS_lINE_BREAK,' ',content)

    content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp)
    content_temp = re.sub(PATTERN_FIND_SPACE_AFTER_INDEX,"\n",content_temp)
    content_temp = re.sub(r" +",' ',content_temp)

    content_temp = re.sub(r"\(cid:\d*\)",'',content_temp)

    content_temp = re.sub(PATTERN_FIND_PAGE_NUMBER,'',content_temp)
    content_temp = re.sub(PATTERN_FIND_WORD_SPLITED,'',content_temp)
    
    content_temp = content_temp.strip()  

    return content_temp    


def get_indices_end_position(data):
    return data.find("Autores")
    

def get_indices(data):
 
    end_indices = get_indices_end_position(data)

    small_data = data[:end_indices] ### Devided data for getting indices, with this i get all data until last index.

    indices_iter = re.finditer(PATTERN_FIND_INDICES,small_data) #Iterable object that contain start, end position and also the matching string of each index
    indices_list = []
    
    for i, index_pos in enumerate(indices_iter):
        index_striped = (index_pos.group().strip()).upper()
        indices_list.append(index_striped)
        print(index_striped)

    return indices_list
>>>>>>> 5cbc346ee369f642c5c4dcb7fcedc61e9872c778

def get_titles(cases_list):
    titles_list = []
    for num in range(len(cases_list)-1):
        matched = re.search(r".*$",cases_list[num]) #Finding las line, may be a title
        title = matched.group().strip()
        titles_list.append(title)
    
<<<<<<< HEAD
    print(len(titles_list)-1) 
    return titles_list

def extract_all_cases(file_root):
    data = get_pdf_data(file_root)
    cases_list = split_all_cases(data)
    titles_list = get_titles(cases_list)
    new_dictionary=dict()

    for title, case in zip(titles_list, cases_list[1:]):
        
        clinical_case = re.sub(r".*$",'',case) #deleting last line ,maybe a title
        new_dictionary[title] = clinical_case

    return new_dictionary

def split_cases_by_paragraphs(cases_dict):
    new_cases_dict = dict()

    for key ,value in cases_dict.items():
        case_splited_list = []
        for num_p in range(len(case_paragraphs)-1):
            position1 = value.find(case_paragraphs[num_p])
            position2 = value.find(case_paragraphs[num_p+1])
            paragraphs = value[position1:position2]           
            case_splited_list.append(paragraphs)
        new_cases_dict[key] =case_splited_list

    return new_cases_dict       

def create_cases_dict(file_root):

    cases_list = extract_all_cases(file_root)
    cases_dict_in_paragraphs = split_cases_by_paragraphs(cases_list) 
    return cases_dict_in_paragraphs

=======
    string_index1 = indices[0]
    start_case = data.find(indices[0])
    
    for index_num in range(len(indices)-1):
        string_index2 = indices[index_num+1]
        if not string_index2 in data:
            string_index2 = string_index2.replace(". ",".\n")
            print(":::::::::::::::::::::::::",string_index2)
            if not string_index2 in data:
                print("\n\n-----------------\n",index_num," ",indices[index_num], " ===> Couldn't find ant case.")
        

        end_case = data.find(string_index2)
        if start_case > end_case:
            end_case = data.rfind(string_index2)
            
        dictionary[string_index1] = data[start_case:end_case]
        
        print("==========================>\n\n")
        print(start_case, " - ",end_case)
        print("index1--->",string_index1,"\n","index2---->",string_index2,"\n",len(data[start_case:end_case]))
        start_case = end_case
        string_index1 = string_index2

        
    return dictionary       

def extract_all_cases(file_root):

    data = get_pdf_data(file_root)
    indices = get_indices(data)
    list_of_all_cases = split_all_cases(data,indices)

    return list_of_all_cases




def main(arguments):
    if not len(arguments) == 2:
        print("Expected 1 argument, but you are passing " + str(len(arguments)-1))
    file_root = arguments[1]
    cases_dictionary = extract_all_cases(file_root)
    i = 0
    for key , value in cases_dictionary.items():
        i += 1
        file = open("data.txt","a+")
        file.write("--->"+str(i) +"\n"+value)
        
if __name__== "__main__":
      main(sys.argv)
>>>>>>> 5cbc346ee369f642c5c4dcb7fcedc61e9872c778
