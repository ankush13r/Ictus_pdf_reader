import logging
import re
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


logger.info("Creating constants and patterns for regex.") #logging


GENDER= {"Hombre":["una paciente","mujer","femenino","fumadora",],"Mujer":["varón","un paciente","el paciente","hombre","fumador"]}
logger.info("Grabbed -> " + repr(GENDER)) #logging

PATTERN_FIND_AGE = r"(?<=de\s)?(\d\d)(\s?años|\smeses)"
logger.info("Grabbed -> " + PATTERN_FIND_AGE) #logging

PATTERN_REPLACES_lINE_BREAK =r"((?<=[^\n])\n)|\x0c" 
logger.info("Grabbed -> " + PATTERN_REPLACES_lINE_BREAK) #logging
# Pattern to replace a single {line break} by a {space} because all pdf conten all data in {table format},
# So, if there is single line break it will findout, which we need to replace by a space.

PATTERN_FIND_CASE_START_PAGE = r".*[^\.](?=\.{6,})"
logger.info("Grabbed -> " + PATTERN_FIND_CASE_START_PAGE) #logging
# Pattern for finding indexes. In pdf all idexes finish with ...... minimum 6 point (ej: any index ...........)
# The patter will just look for all lines those have this format (any index .....),
# from those lines it will get all indices, but without any points << .... >>

PATTERN_FIND_PAGE_NUMBER = r"-\s\d+\s-"
logger.info("Grabbed -> " + PATTERN_FIND_PAGE_NUMBER)  #logging
# Pattern for finding page number, it must be in format <<- ## - >> .

PATTERN_FIND_WORD_DIVIDED = r"- (?=\w)"
logger.info("Grabbed -> " + PATTERN_FIND_WORD_DIVIDED) #logging
# Pattern for find words those are divided by (-). << Wor- d >>. 
# Because, so many words are written at the end of the line with - and continued in next line

PATTERN_FIND_MANY_SPACE = r" +|"+chr(160)+"+"
logger.info("Grabbed -> " + PATTERN_FIND_MANY_SPACE) #logging
# Pattern for finding more all none printable characters (may be a space) repeated. chr(160) is also a rare none printable character found in pdf

PATTERN_RARE_CARACTERS = r"\(cid:\d*\)"
logger.info("Grabbed -> " + PATTERN_RARE_CARACTERS) #logging
#Pattern for find (cid:##). Because PDF CONVERTER  converts graphic to a code like (cid:##)

PATTERN_FIND_HEADER = r".*CONCURSO DE CASOS CLÍNICOS.*20\d\d"
logger.info("Grabbed -> " + PATTERN_FIND_HEADER) #logging
#Pattern for finding pdf header like (CONCURSO DE CASOS CLÍNICOS .... 2015)

logger.info("Creating object type tuple (case_paragraphs) with each paragraph's title") #logging
case_paragraphs = ("Anamnesis","Exploración física","Pruebas complementarias","Diagnóstico","Tratamiento","Evolución", "DISCUSIÓN","BIBLIOGRAFÍA","Figura 1.")

logger.info("All constants and pattern are saved.") #logging

