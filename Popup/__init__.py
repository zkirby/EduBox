'''
Popup main build file

houses mostly just housekeeping items
'''
def popup_build():
    '''Puts all the file infor and such 
    together for the dialogs to use'''
    global about_contents, mechanics_contents, credits_contents
    
    line_num = 1
    
    #Open Files
    try:
        about_file = open('Resources/General Files/About', 'r')
    except Exception, e:
        print("Failure Opening Files for Dialogs: "+e)
    
    #Put Content Together
    about_contents = ''''''; mechanics_contents = ''''''; credits_contents = ''''''
    for item in about_file:
        if line_num == 1:
            about_contents+=item
            if "EN_D" in item:
                about_contents = about_contents[:-6]
                line_num = 2
        elif line_num == 2:
            mechanics_contents+=item
            if 'EN_D2' in item:
                mechanics_contents = mechanics_contents[:-7]
                line_num = 3
        elif line_num == 3:
            credits_contents+=item
    

    #Close Files
    try:
        about_file.close()
    except Exception, e:
        print("Faliure closing files for Dialogs: "+str(e))
        
    return about_contents, mechanics_contents, credits_contents