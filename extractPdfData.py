#You must upgrade setuptools and install padfminer librery first.

"""pip install --upgrade setuptools"""
"""pip install pdfminer3K"""

from io import open 
import re
import pdf_reader as rPDF
import sys
from pdfminer.pdfinterp import PDFResourceManager , process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

PATTERN_REPLACS_lINE_BREAK =r"((?<=[^\n])\n)|\x0c"  
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

class Data_extract:
    def readPDF(file_root):
        pdf_file = open(file_root,"rb") ###
        content = pdf_file.read()
        resource_maneger = PDFResourceManager()
        ret_string = StringIO()
        laparams = LAParams()
        device = TextConverter(resource_maneger,ret_string, laparams=laparams)      
        process_pdf(resource_maneger,device,pdf_file)
        device.close()
        content = ret_string.getvalue()
        ret_string.close()
        return content

    def fix_up_content(content):      
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

    def make_case_dict(cases_list):
        dictionary=dict()
        for num in range(len(cases_list)-1):
            if len(cases_list[num]) == 0:
                pass
            else:
                matched = re.search(r".*$",cases_list[num]) #Finding last line, must be the title of next case.
                title = matched.group().strip()
                clinical_case = re.sub(r".*$",'',cases_list[num+1]) #picking up next case, because the case's title was saved in prevoius case 
                diagnostico_clinico_pos = clinical_case.find("Diagnóstico clínico")
                if diagnostico_clinico_pos != -1:
                    anamnesis_pos = clinical_case.find("Anamnesis")
                    clinical_case = clinical_case[:diagnostico_clinico_pos] + clinical_case[anamnesis_pos:]
                clinical_case_striped = clinical_case.strip()
                dictionary[title] = clinical_case_striped       
        return dictionary

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

