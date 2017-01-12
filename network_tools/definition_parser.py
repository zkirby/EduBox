'''
Created on Jan 19, 2016

@author: zachary

@purpose: Contains a web scraper for grabbing online definitions
'''
import urllib
import re
import time

def definition_search(word, display=False):
    '''Scraps the online merriam-webster 
    dictionary for a dictionary definition'''
    global value_return, definitions_list

    #Make Sure Word will work
    word = str(word).lower()
    url = ("http://www.merriam-webster.com/dictionary/"+word)
    definitions_list = []
    
    #Start Patter Compiling
    try:
        custom_pattern_list = ['<', '>', '/', 'class="v"', '&lt', '&gt', 'class="vi"']
        htmlfile = urllib.urlopen(url)
        htmltext = htmlfile.read()
        definition_body = make_new_pattern('<span>(.+?)</span>', htmltext)
    except Exception, e:
        print("Falure To Compile Pattern Recognition: "+str(e))

    if htmltext != None:
        
        #Start Stripping/ Beautification of Definitions
         try:
            
            #Search For Only the Definitions
            for line_of_text in definition_body:
                if '<strong>' in line_of_text:
                    marker = line_of_text.find('</strong>')
                    refined_definition = line_of_text[marker+12:]
                    new_remove_pattern = make_new_pattern('<(.+?)>', line_of_text)
                    remove_list = []
                    
                    #Remove Unwanted Tags
                    for tag in new_remove_pattern:
                        remove_list.append(tag)
                    for tag in remove_list:
                        if tag in refined_definition:
                            refined_definition = refined_definition.replace(tag,"")
                    
                    #Check the tags the Parser missed
                    for unwanted_object in custom_pattern_list:
                        if unwanted_object in refined_definition:
                            refined_definition = refined_definition.replace(unwanted_object,"")
                    
                    #Finishing Touches 
                    refined_definition = punctuation_handler(refined_definition)
                    
                    if value_return == True:
                        definitions_list.append(refined_definition)  
        
            #Circle Through the Sentences and Returns the list                
            if len(definitions_list) > 0:
                if display == True:
                    for line in definitions_list:
                        line = line[0].upper() + line[1:]
                        print(line+"\n")
                return definitions_list
            else:
                raise NameError("!!That Word: "+word+" was not registered in this dictionary!!")
                        
         except Exception, e:
             print("Error stripping or beautifying definition: \n"+str(e))
    else:
        raise NameError("The Word you typed raised an error")
                
def make_new_pattern(pattern, location):
    '''Used to compile new patterns for 
    stripping or concatinating in the definitions
    body of text'''    
    try:
        pareser_pattern = re.compile(pattern)
        return re.findall(pareser_pattern, location)
    except Exception, e:
        print("Failed To Produce a Pattern: "+str(e))
        
def punctuation_handler(word):
    global value_return, definitions_list, non_local_stop
    '''Handles all of the semi-colon/ colon stripping
    a suprising amount of the code requires this'''
    try:
        #'Easy' Cleaning
        other_half = ""; half_word = ""; value_return = True; cach_list = []; cach_count = 0; vr = 0
        new_word = word.rstrip()
        if new_word.endswith(";"):
            new_word = new_word[:-1]
        if new_word.endswith(".") == False and new_word.endswith("?") == False:
            new_word = new_word+"."
        new_word = new_word.replace(" ;", "; ")
        new_word = new_word.replace("  ;", "; ")
        
        #'Complex' punctuation cleaning
        for i, char in enumerate(new_word):
            if char == ";":
                if new_word[i] == new_word[i-1]:
                    new_word = new_word[:i-1] + new_word[i:]
                if new_word[i-1] == ".":
                    new_word = new_word[:i-1] + new_word[i:]
            if char == ":":
                replaced_char=(i+1)
                new_word = new_word.replace(new_word[replaced_char], "\n")
        
        new_word = new_word.replace(" ; ", "; ")
        
        #Compound Check and Cach Constructor
        if ":" in new_word:
            new_word = new_word.replace(":", "^")
            cach_count = new_word.count("^")
        for i, char in enumerate(new_word):
            if char == "^":
                cach_list.append(i)
        
        #Construct Sentences If they fail compound check
        if cach_count >= 1:
            value_return = False
            temp_word = new_word[:cach_list[0]]
            temp_word = temp_word.rstrip(); temp_word = temp_word.lstrip()
            definitions_list.append(temp_word)
            for list_count in range(len(cach_list)):
                if list_count < (len(cach_list)-1):
                    temp_word = new_word[cach_list[list_count]+4:cach_list[list_count+1]]
                    temp_word = temp_word.rstrip(); temp_word = temp_word.lstrip()
                    definitions_list.append(temp_word)
                if list_count == (len(cach_list)-1):
                    temp_word = new_word[cach_list[list_count]+4:]
                    temp_word = temp_word.rstrip(); temp_word = temp_word.lstrip()
                    definitions_list.append(temp_word)
                                
        return new_word
        
    except Exception, e:
        print("Failed To Punctuate Correctly: "+str(e))
        







    
