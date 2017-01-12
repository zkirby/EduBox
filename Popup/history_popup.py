'''
Created on Feb 4, 2016

@author: zachary

History Popup, containts the mechanics for the history workbench
'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from network_tools import history_definition_parser as hdp

def file_system():
    '''Puts all the file infor and such 
    together for the dialogs to use'''    
    list_count = 0
    names_list2 = []; terms_names_list2 = [[]]; terms_content_list2 = [[]]
    
    #Open Files
    try:
        names_file = open('Resources/History Files/terms_lists_names', 'r')
        terms_content_file = open('Resources/History Files/terms_lists', 'r')
    except Exception, e:
        print("Failure Opening Files for Dialogs: "+e)
    
    #Put Content Together
    for name in names_file:
        names_list2.append(name[:-1])
    for term in terms_content_file:
        item = term[:-1]
        if item.endswith("%"):
            terms_names_list2[list_count].append(item[:-1])
        elif item.endswith("^"):
            terms_content_list2[list_count].append(item[:-1])
        elif item == "__N$ew0__":
            terms_content_list2.append([])
            terms_names_list2.append([])
            list_count+=1

    #Close Files
    try:
        names_file.close()
        terms_content_file.close()
    except Exception, e:
        print("Faliure closing files for Dialogs: "+str(e))
        
    return names_list2, terms_names_list2, terms_content_list2

class HistoryPopUp(Gtk.Dialog):
    
    def __init__(self, parent):
        global names_list, terms_names_list, terms_content_list
        Gtk.Dialog.__init__(self, "History Workstation", parent, Gtk.DialogFlags.MODAL, (
            "Write Data", Gtk.ResponseType.CANCEL, 
            "Finished", Gtk.ResponseType.OK))
        
        self.set_default_size(400, 400)
        self.set_border_width(30)
        self.start = 0
        self.index_next = 0
        self.arrow_mode = 0
        area = self.get_content_area()
        names_list, terms_names_list, terms_content_list = file_system()
        
        
        #Setup Componets
        grid = Gtk.Grid()
        self.term_entry = Gtk.Entry()
        self.term_label = Gtk.Label("Input Term")
        self.term_button_left = Gtk.Button()
        self.term_button_right = Gtk.Button()
        self.view_switch_label = Gtk.Label("View Toggle")
        self.space_filler = Gtk.Label("               ")
        self.space_filler_2 = Gtk.Label("               ")
        self.view_switch = Gtk.Switch()
        self.help_button = Gtk.Button("Define Term")
        self.new_terms_list_button = Gtk.Button("New List")
        self.add_term_button = Gtk.Button("Add Term")
        self.new_list_done_button = Gtk.Button("Done Adding")
        self.view_area_label = Gtk.Label("Definition")
        self.view_area = Gtk.TextView()
        self.view_area_buffer = self.view_area.get_buffer()
        self.term_list_label = Gtk.Label("Choose a Terms List")
        self.term_list_dropdown = Gtk.ComboBoxText()
                
        #Componet Options
        self.view_area.set_editable(False)
        self.button_image_1 = Gtk.Image.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.MENU)
        self.button_image_2 = Gtk.Image.new_from_icon_name("go-next-symbolic", Gtk.IconSize.MENU)
        self.term_button_left.set_image(self.button_image_1)
        self.term_button_right.set_image(self.button_image_2)
        self.view_switch.connect("notify::active", self.on_switch_activated)
        self.view_switch.set_active(False)
        self.make_terms_list()
        #self.view_area.set_wrap_mode(Gtk.WrapMode.WORD)

        #Connections
        self.help_button.connect("clicked", self.help_search)
        self.term_button_left.connect("clicked", self.previous_para)
        self.term_button_right.connect("clicked", self.next_para)
        self.term_list_dropdown.connect("changed", self.display_terms)
        self.new_terms_list_button.connect("clicked", self.new_terms_list)
        
        #Setup Grid (left, top, width, height)
        grid.attach(self.view_area, 10, 2, 40, 14)
        grid.attach(self.view_area_label, 15, 0, 2, 1 )
        grid.attach(self.space_filler, 10, 0, 7, 1)
        grid.attach(self.space_filler_2, 20, 0, 7, 1)
        grid.attach(self.term_label, 1, 0, 1, 1)
        grid.attach(self.term_entry, 1, 2, 2, 1)
        grid.attach(self.term_list_label, 1, 4, 1, 1)
        grid.attach(self.term_list_dropdown, 1, 6, 2, 1)
        grid.attach(self.view_switch_label, 1, 8, 1, 1)
        grid.attach(self.view_switch, 1, 10, 2, 1)
        grid.attach(self.term_button_left, 0, 12, 1, 2)
        grid.attach(self.term_button_right, 2, 12, 1, 2)
        grid.attach(self.help_button, 1, 14, 1, 1)
        grid.attach(self.new_terms_list_button, 1, 16, 1, 1)
        
        area.add(grid)        
        self.show_all()  
    
    def make_terms_list(self):
        global names_list
        self.term_list_dropdown.remove_all()
        for i,name in enumerate(names_list):
            self.term_list_dropdown.insert(i+1, str(i+1), name)
        
    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            self.term_entry.set_visibility(False)
        else:
            self.term_entry.set_visibility(True)
    
    def help_search(self, widget):
        self.arrow_mode = 1
        self.definition_of_word = hdp.definition_search(str(self.term_entry.get_text()))
        self.view_area_buffer.set_text(self.definition_of_word[0])
        
    def next_para(self, widget):
        if self.arrow_mode == 1:
            self.start+=1
            try:
                self.view_area_buffer.set_text(self.definition_of_word[self.start])
            except IndexError, e:
                print("There is no more definition to read: "+str(e))
                self.view_area_buffer.set_text(self.definition_of_word[-1])
                self.start-=1
        elif self.arrow_mode == 2:
            self.index_next+=1
            try:
                self.term_entry.set_text(self.current_term_name[self.index_next])
                self.view_area_buffer.set_text(self.current_term_content[self.index_next])
            except Exception, e:
                print("No more terms left: "+str(e))
                self.term_entry.set_text(self.current_term_name[-1])
                self.view_area_buffer.set_text(self.current_term_content[-1])
                self.index_next-=1

    def previous_para(self, widget):
        if self.arrow_mode == 1:
            self.start-=1
            try:
                if self.start >= 0:
                    self.view_area_buffer.set_text(self.definition_of_word[self.start])
                else:
                    raise IndexError("Error, negatives reached")
            except Exception, e:
                print("Can't go back that far, nothing to read: "+str(e))
                self.view_area_buffer.set_text(self.definition_of_word[0])
                self.start+=1
        elif self.arrow_mode == 2:
            self.index_next-=1
            try:
                if self.index_next >= 0:
                    self.term_entry.set_text(self.current_term_name[self.index_next])
                    self.view_area_buffer.set_text(self.current_term_content[self.index_next])
                else:
                    raise IndexError("Error, negatives reached")
            except Exception, e:
                print("Can't go back that far, nothing to read: "+str(e))
                self.term_entry.set_text(self.current_term_name[0])
                self.view_area_buffer.set_text(self.current_term_content[0])
                self.index_next = 0
    
    def display_terms(self, widget):
        global names_list, terms_names_list, terms_content_list
        
        self.current_item = self.term_list_dropdown.get_active_text()
        if  self.current_item != None:
            current_index = names_list.index(self.current_item)
        else:
            current_index = 0
            
        self.current_term_name = terms_names_list[current_index]
        self.current_term_content = terms_content_list[current_index]
        
        self.arrow_mode = 2
        self.term_entry.set_text(self.current_term_name[0])
        self.view_area_buffer.set_text(self.current_term_content[0])
        
        print(names_list, terms_names_list, terms_content_list)
        print(current_index, self.current_item, self.current_item)
    
    def new_terms_list(self, widget):
        global names_list, terms_names_list, terms_content_list, temp_name, temp_def, temp_term
        dialog = NewListSupport(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            try:
                names_list.append(temp_name)
                terms_names_list.append(temp_term)
                terms_content_list.append(temp_def)
                self.make_terms_list()
            except Exception, e:
                print("Failed to Add list to Current Database: "+str(e))
        elif response == Gtk.ResponseType.CANCEL:
            print("List Creation Canceled")
            
        dialog.destroy()


def history_popup_finished():
    '''Cleans up the history popup stores 
    all of the new terms lists in a file'''
    global names_list, terms_names_list, terms_content_list
    
    #Open Files
    try:
        write_names_file = open('Resources/History Files/terms_lists_names', 'w')
        write_content_file = open('Resources/History Files/terms_lists', 'w')
    except Exception, e:
        print("Failure Opening Files To Save Data: "+e)
    
    #Write Data to File
    try:
        for name in names_list:
            write_names_file.write(name+"\n")
        for i,listOne in enumerate(terms_names_list):
            for j,item in enumerate(listOne):
                content = terms_content_list[i][j]+"^\n"
                write_content_file.write(item+"%\n")
                write_content_file.write(content)
            if terms_names_list[i] != terms_names_list[-1]:
                write_content_file.write("__N$ew0__\n")                
    except Exception, e:
        print("Error Writing data to file: "+str(e))
    
    #Close Files
    try:
        write_names_file.close()
        write_content_file.close()
    except Exception, e:
        print("Faliure closing files at history cleanup: "+str(e))
        
class NewListSupport(Gtk.Dialog):
    
    def __init__(self, parent):
        global temp_name, temp_def, temp_term
        Gtk.Dialog.__init__(self, "New List Maker", parent, Gtk.DialogFlags.MODAL, (
            "Cancel", Gtk.ResponseType.CANCEL, 
            "Add List", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 400)
        self.set_border_width(30)
        area = self.get_content_area()
        self.list_size = 0; self.name_set = True
        temp_name = ""; temp_def = []; temp_term = []
        
        #Add Componets
        grid = Gtk.Grid()
        self.entry_label = Gtk.Label("Term Name")
        self.define_label = Gtk.Label("Define Term")
        self.name_entry_label = Gtk.Label("List Name")
        self.define_area = Gtk.TextView()
        self.define_area_buffer = self.define_area.get_buffer()
        self.add_term_button = Gtk.Button("Add")
        self.term_area_entry = Gtk.Entry()
        self.name_entry = Gtk.Entry()
        self.count_text = Gtk.Label("List Size: ")
        self.last_item_name = Gtk.Label("Last Term: ")
        
        #Options
        self.define_area.set_editable(True)
        
        #Connections
        self.add_term_button.connect("clicked", self.add_term_to_list)
        
        #Grid Layout (left, top, width, height)
        grid.attach(self.name_entry_label, 1, 0, 1, 1)
        grid.attach(self.name_entry, 1, 1, 1, 1)
        grid.attach(self.entry_label, 1, 2, 1, 1)
        grid.attach(self.term_area_entry, 1, 3, 1, 1)
        grid.attach(self.add_term_button, 1, 4, 1, 1)
        grid.attach(self.count_text, 1, 5, 1, 1)
        grid.attach(self.last_item_name, 1, 6, 1, 1)
        grid.attach(self.define_label, 3, 0, 1, 1)
        grid.attach(self.define_area, 3, 1, 20, 20)

        area.add(grid)        
        self.show_all() 
        
        
    def add_term_to_list(self, widget):
        global names_list, terms_names_list, terms_content_list, temp_name, temp_def, temp_term
        
        try:
            self.list_size+=1
            start, end = self.define_area_buffer.get_bounds()
            list_name = self.name_entry.get_text()
            term_name = self.term_area_entry.get_text()
            term_defin = self.define_area_buffer.get_text(start, end, False)
            
            self.name_entry.set_editable(False)
            if self.name_set == True:
                if list_name != None:
                    temp_name = list_name
                else:
                    temp_name = "New List"
                self.name_set = False
            else:
                print("Name Set")
            
            if term_name != None:
                temp_term.append(term_name)
            else:
                temp_term.append("Unnamed Term")
            
            if term_defin != None:
                temp_def.append(term_defin)
            else:
                temp_def.append("This Term Is Undefined")
            
            self.last_item_name.set_text("Last Term: "+str(term_name))
            self.count_text.set_text("List Size: "+str(self.list_size))
            self.term_area_entry.set_text("")
            self.define_area_buffer.set_text("")
                        
        except Exception, e:
            print("Error Adding Item: "+str(e))


