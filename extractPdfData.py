from io import open 
import re
import pdf_reader as rPDF
import pdf_to_text
import sys


PATTERN_REPLACS_lINE_BREAK =r"((?<=[^.\n])\n)|\x0c"  
# Pattern for replace a single {line break} by a {space} because all pdf conten all data in {table format},
# So, if there is single line break it will findout, which we need to replace by a space.


PATTERN_FIND_CASE_START_PAGE = r".*[^\.](?=\.{6,})"
# Pattern for find indexes. In pdf all idexes finish with ...... minimum 6 point (ej: any index ...........)
# The patter will just look for all lines those have this format (any index .....),
# from those lines it will get all indices, but without any points (....)

PATTERN_FIND_SPACE_AFTER_INDEX = r"(?<=\.{6})\s(?=\w)"
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
    out_put = open("data_parsed.txt","w")
    out_put.write(final_content)

    return final_content
  


def split_all_cases(data):
    list = data.split("Supervisión:")   
    print("Total number of clinical cases: ", len(list)-2)
    return list      


def get_titles(cases_list):
    titles_list = []
    for num in range(len(cases_list)-1):
        matched = re.search(r".*$",cases_list[num]) #Finding las line, may be a title
        title = matched.group().strip()
        titles_list.append(title)
    return titles_list

def extract_all_cases(file_root):
    data = get_pdf_data(file_root)
    cases_list = split_all_cases(data)
    titles_list = get_titles(cases_list)
    new_dictionary=dict()

    for title, case in zip(titles_list, cases_list[1:]):  
        clinical_case = re.sub(r".*$",'',case) #deleting last line ,maybe a title
        if len(clinical_case) == 0:
            pass
        else:
            new_dictionary[title] = clinical_case
    return new_dictionary

def split_cases_by_paragraphs(cases_dict):
    new_cases_dict = dict()

    for key ,value in cases_dict.items():
        case_splited_list = []
        position1 = 0

        for num_p in range(len(case_paragraphs)):
            position2 = value.find(case_paragraphs[num_p])
            paragraphs = value[position1:position2]           
            case_splited_list.append(paragraphs)
            position1 = position2
        new_cases_dict[key] =case_splited_list

    return new_cases_dict       

def create_cases_dict(file_root):

    cases_list = extract_all_cases(file_root)
    cases_dict_in_paragraphs = split_cases_by_paragraphs(cases_list) 
    return cases_dict_in_paragraphs