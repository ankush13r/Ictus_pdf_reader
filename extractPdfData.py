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
import logging

#DEBUG ,INFO, WARNING, ERROR, CRITICAL
#----------------------------------------------------#
#----------------logging setting---------------------#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#Formatter handdler
console_formatter = logging.Formatter('%(levelname)s:%(name)s: <<%(message)s>>')
file_formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s <<%(message)s>>')
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


logger.info("Creating patterns for regex.") #logging

PATTERN_REPLACES_lINE_BREAK =r"((?<=[^\n])\n)|\x0c" 
logger.info("Created -> " + PATTERN_REPLACES_lINE_BREAK) #logging
# Pattern to replace a single {line break} by a {space} because all pdf conten all data in {table format},
# So, if there is single line break it will findout, which we need to replace by a space.

PATTERN_FIND_CASE_START_PAGE = r".*[^\.](?=\.{6,})"
logger.info("Created -> " + PATTERN_FIND_CASE_START_PAGE) #logging
# Pattern for finding indexes. In pdf all idexes finish with ...... minimum 6 point (ej: any index ...........)
# The patter will just look for all lines those have this format (any index .....),
# from those lines it will get all indices, but without any points << .... >>

PATTERN_FIND_PAGE_NUMBER = r"-\s\d+\s-"
logger.info("Created -> " + PATTERN_FIND_PAGE_NUMBER)  #logging
# Pattern for finding page number, it must be in format <<- ## - >> .

PATTERN_FIND_WORD_DIVIDED = r"- (?=\w)"
logger.info("Created -> " + PATTERN_FIND_WORD_DIVIDED) #logging
# Pattern for find words those are divided by (-). << Wor- d >>. 
# Because, so many words are written at the end of the line with - and continued in next line

PATTERN_FIND_MANY_SPACE = r" +|"+chr(160)+"+"
logger.info("Created -> " + PATTERN_FIND_MANY_SPACE) #logging
# Pattern for finding more than one space repeated. chr(160) is also a rare none printable character found in pdf

PATTERN_RARE_CARACTERS = r"\(cid:\d*\)"
logger.info("Created -> " + PATTERN_RARE_CARACTERS) #logging
#Pattern for find (cid:##). Because PDF CONVERTER  converts graphic in a code like (cid:##)

PATTERN_FIND_HEADER = r".*CONCURSO DE CASOS CLÍNICOS.*20\d\d"
logger.info("Created -> " + PATTERN_FIND_HEADER) #logging
#Pattern for finding pdf header like (CONCURSO DE CASOS CLÍNICOS.*2015)

logger.info("Creating object type tuple (case_paragraphs)") #logging
case_paragraphs = ("Anamnesis","Exploración física","Pruebas complementarias","Diagnóstico","Tratamiento","Evolución", "DISCUSIÓN","BIBLIOGRAFÍA","Figura 1.")

class Data_extract:
    def readPDF(file_root):
        pdf_file = open(file_root,"rb")
        logger.info("PDF file opened as binary (rb).") #logging
        resource_maneger = PDFResourceManager()
        logger.info("Created resource maneger for Text Converter.") #logging
        ret_string = StringIO()
        logger.info("Created StringIO as ret_string to save pdf text.") #logging
        laparams = LAParams(line_overlap=0.5, char_margin=1.0, line_margin=0.5, word_margin=0.1)
        logger.info("Created LAParams as laparams for definig character, word and line margin .") #logging
        device = TextConverter(resource_maneger,ret_string, laparams=laparams)      
        logger.info("Created TextConverter as device.") #logging
        process_pdf(resource_maneger,device,pdf_file)
        logger.info("Processed Converted PDF File into text .") #logging
        device.close()
        logger.info("Device closed.") #logging
        content = ret_string.getvalue()
        logger.info("Saved all conteint as string into a varibale called content.") #logging      
        ret_string.close()
        logger.info("ret_string closed.") #logging
        return content

    def fix_up_content(content):
        logger.info("Fixing up all content") #logging
        content_temp = re.sub(PATTERN_REPLACES_lINE_BREAK,' ',content) #Replace line break by a space.
        logger.info("Replaced some line breaks by space") #logging
        content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp) #Strip all spaces those are repeated.
        logger.info("Deleted all repeated space") #logging

        content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp) #Strip all spaces those are repeated, again
        content_temp = re.sub(PATTERN_RARE_CARACTERS,'',content_temp) # Deleting all rare caracter as  (cid:32)
        content_temp = re.sub(PATTERN_FIND_PAGE_NUMBER,'',content_temp)
        content_temp = re.sub(PATTERN_FIND_HEADER,'',content_temp)
        final_content = re.sub(PATTERN_FIND_WORD_DIVIDED,'',content_temp)

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

