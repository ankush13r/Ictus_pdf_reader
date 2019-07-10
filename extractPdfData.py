#You must upgrade setuptools and install padfminer librery first.

"""pip install --upgrade setuptools"""
"""pip install pdfminer3K"""

from io import open 
import re
import sys
from pdfminer.pdfinterp import PDFResourceManager , process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import logging
from constants import case_paragraphs,PATTERN_REPLACES_lINE_BREAK, PATTERN_FIND_CASE_START_PAGE, PATTERN_FIND_PAGE_NUMBER,\
PATTERN_FIND_WORD_DIVIDED, PATTERN_FIND_MANY_SPACE,PATTERN_RARE_CARACTERS,PATTERN_FIND_HEADER

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
#logger instead of logging.
#---------------logging setting--------------------#
#--------------------------------------------------#


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
        logger.info("Saved all content as string into a variable called content.") #logging      
        ret_string.close()
        logger.info("ret_string closed.") #logging
        return content

    def fix_up_content(content):
        logger.info("Fixing up all content") #logging
        logger.info("Replacing some line breaks by space") #logging
        content_temp = re.sub(PATTERN_REPLACES_lINE_BREAK,' ',content) #Replace line break by a space.
        logger.info("Deleting all repeated space") #logging
        content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp) #Strip all spaces those are repeated.
        logger.info("Deleting all characters like (cid:32).") #logging
        content_temp = re.sub(PATTERN_RARE_CARACTERS,'',content_temp) # Deleting all rare character as  (cid:32)
        logger.info("Deleting all page number. Ex: - 10 -") #logging
        content_temp = re.sub(PATTERN_FIND_PAGE_NUMBER,'',content_temp)
        logger.info("Deleting all page headers (CONCURSO DE CASOS CLÍNICOS. ..... 201#)") #logging
        content_temp = re.sub(PATTERN_FIND_HEADER,'',content_temp)
        logger.info("putting together all words those which are separated by hyphen. (Ex: Wor- d)") #logging
        final_content = re.sub(PATTERN_FIND_WORD_DIVIDED,'',content_temp)
        logger.info("Deleting all repeated space again.") #logging
        content_temp = re.sub(PATTERN_FIND_MANY_SPACE,' ',content_temp) #Strip all spaces those are repeated again.
        out_put = open("data_parsed.txt","w")
        out_put.write(final_content)
        return final_content
    
    def split_all_cases(data):
        logger.info("Seprating all case by Supervisón.") #logging      
        list = data.split("Supervisión:")
        logger.info("Total number of clinical cases: "+ str(len(list)-2)) #logging
        return list      

    def make_case_dict(cases_list):
        dictionary=dict()
        
        logger.info("Making a loop to make a dictionary, title as a key.") #logging
        for num in range(len(cases_list)-1):
            if len(cases_list[num]) == 0:
                logger.warning("Nothing to do, because case length was 0: case nº {num+1}.") #logging
                pass
            else:
                matched = re.search(r".*$",cases_list[num]) #Finding last line, must be the title of next case.
                title = matched.group().strip()
                clinical_case = re.sub(r".*$",'',cases_list[num+1]) #picking up next case, because the case's title was saved in prevoius case 
                diagnostico_clinico_pos = clinical_case.find("Diagnóstico clínico") #Getting the position of a word (Diagnóstico clínico).
                #If have been found "Diagnóstico clínico" 
                # than it will save all string except the Diagnóstico clínico paragraph
                # Otherwise, nothing to do.
                if diagnostico_clinico_pos != -1:
                    anamnesis_pos = clinical_case.find("Anamnesis")
                    clinical_case = clinical_case[:diagnostico_clinico_pos] + clinical_case[anamnesis_pos:]
                clinical_case_striped = clinical_case.strip()
                logger.info(f"Saving to the dictionary: case nº {num+1}.") #logging             
                dictionary[title] = clinical_case_striped  
        return dictionary

    def split_cases_by_paragraphs(cases_dict):
        new_cases_dict = dict()

        logger.info(f"Making a loop of all cases to divide all paragraphs by it's title.\nf{case_paragraphs}") #logging
        for key ,value in cases_dict.items():
            case_divided_list = []
            position1 = 0 
            #A loop for getting all paragraphs separated by the start and end position. 
            # Positions are gotten by finding the  title of each paragraphs, 
            # those that are saved as a object type tuple in a variable called case_paragraphs
            for num_paragraph in range(len(case_paragraphs)):
                position2 = value.find(case_paragraphs[num_paragraph])
                paragraphs = value[position1:position2]           
                if num_paragraph < len(case_paragraphs)-1:
                    logger.info(f"Appending the paragraph into a temporally variable type list, titled by {case_paragraphs[num_paragraph]}") #logging
                case_divided_list.append(paragraphs)
                position1 = position2
            logger.info(f"Saving all data to a dictionary, the title as key and all paragraphs divided as value") #logging  
            new_cases_dict[key] =case_divided_list
        return new_cases_dict       

