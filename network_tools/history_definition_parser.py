'''
Created on Jan 21, 2016

@author: zachary
'''
import urllib
import re
import time

def definition_search(word):
    '''Scraps the online wiki data base
    for articles on the appropriate topic'''
    global value_return, definitions_list

    #Make Sure Word will work
    word = str(word).replace(" ", "_")
    url = ("https://en.wikipedia.org/wiki/"+word)
    definitions_list = []
    return_list = []
    
    #Start Patter Compiling
    try:
        custom_pattern_list = ['<', '>', '/', 'class="v"', '&lt', '&gt', 'class="vi"', "&#160;"]
        htmlfile = urllib.urlopen(url)
        htmltext = htmlfile.read()
        definition_body = make_new_pattern('<p>(.+?)</p>', htmltext)
    except Exception, e:
        print("Falure To Compile Pattern Recognition: "+str(e))

    try:
        #Search For Only the Definitions
        for line_of_text in definition_body:  
            #print("Given: "+line_of_text)         
            html_pattern = make_new_pattern('<(.+?)>', line_of_text)
    
            #Remove Unwanted Tags
            html_extra_remove_pattern = pattern_format(html_pattern)
            
            remove_list = []
            for tag in html_extra_remove_pattern:
                remove_list.append(tag)
            for tag in remove_list:
                if tag in line_of_text:
                    line_of_text = line_of_text.replace(tag,"")
            
            #Check the tags the Parser missed
            for unwanted_object in custom_pattern_list:
                if unwanted_object in line_of_text:
                    line_of_text = line_of_text.replace(unwanted_object,"")
            
            #Finishing Touches 
            refined_definition = punctuation_handler(line_of_text)
            
            if refined_definition != None:
                return_list.append(refined_definition)
            else:
                print("Wiki Parser recieved None Type value")

    except Exception, e:
        print("Error stripping or beautifying definition: \n"+str(e))
    
    if return_list != None:
        return return_list
    else:
        print("!!That Word: "+word+" was not registered in this dictionary!!")
    
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
    '''Handles all of the semi-colon/ colon stripping
    a suprising amount of the code requires this'''
    period_list = []
    replace_dict = {" y ":" by "}
    remove_brac = False
    remove_brac_added = False
    revised_word = ""
        
    try:
        #'Easy' Cleaning
        for repl in replace_dict:
            new_word = word.replace(repl, replace_dict[repl])
        new_word = new_word.rstrip()
        
        #Check For Unnecessary quotes 
        for i, char in enumerate(new_word):
            if char == ".":
                period_list.append(i)
        if new_word.endswith(":") and len(period_list) > 0:      
            stop_to = period_list[-1]  
            new_word = new_word[:stop_to]
        elif new_word.endswith(":") and len(period_list) == 0:
            print("Paragraph-- '"+word+"' --Deleted")
            new_word = ""
        
        #Check Start and End
        if new_word.endswith(".") == False and ((new_word.endswith("?") or new_word.endswith("!")) == False):
            new_word+="."
        next_char = 1
        while new_word[0].isalpha() == False and new_word[0].isdigit() == False:
            new_word = new_word[next_char:]
            next_char+=1
        
        #Remove Sitations
        temp_cach = new_word.split()
        for i, word in enumerate(temp_cach):
            word2 = word
            if ("[" and "]") in word:
                for j, char in enumerate(word):
                    if char.isdigit():
                        start = word.index("[")
                        end = word.index("]")
                        temp_cach[i] = word2[:start] + word2[end:]
                        remove_brac = True
            if word.startswith("i") and len(word) > 1:
                if word[1].isupper():
                    temp_cach[i] = word[1:]
            if word.startswith("a") and len(word) > 1:
                if word[1].isupper():
                    temp_cach[i] = word[1:]
            if remove_brac == True:
                word2 = word2.replace("[", ""); word2 = word2.replace("]", "")
                temp_cach[i] = word2
                remove_brac = False; remove_brac_added = True
        for word21 in temp_cach:
            revised_word+=(word21 +" ")
        if remove_brac_added == True:
            revised_word = revised_word[:-2]
            
                                                
        return revised_word
        
    except Exception, e:
        print("Failed To Punctuate Correctly: "+str(e))
        
def pattern_format(pattern):
    '''Formats the pattern to 
    help with processing'''
    try:
        for object in pattern:
            if "/" in object:
                pattern.remove(object)
                pattern.append(object)
        if "i" in pattern: 
            pattern.remove("i")
        if "a" in pattern:
            pattern.remove("a")
            
        return pattern
    
        print(pattern)
    except Exception, e:
        print("Error Formating pattern: "+str(e))




