'''
Created on Apr 3, 2016

@author: zachary
'''
import gi, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess as sp

override_prompt = "A file with this name already exists, would you like to Override this file?"

class SaveFilePopUp(Gtk.Dialog):
    
    def __init__(self, parent):
        global data_content, data_names
        Gtk.Dialog.__init__(self, "Save File", parent, Gtk.DialogFlags.DESTROY_WITH_PARENT,(
            "Write Data", Gtk.ResponseType.CANCEL, 
            "Finished", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 100)
        self.set_border_width(30)
        area = self.get_content_area()   
        
        #Setup Componets
        grid = Gtk.Grid()
        self.name_label = Gtk.Label("Name")
        self.name_entry = Gtk.Entry()
        self.name_button = Gtk.Button("Save")
        self.status_label = Gtk.Label("Status: ")
    
        #Connections
        self.name_button.connect('clicked', self.attempt_save)
        
        #Build Grid For Data (left, top, width, height)
        grid.attach(self.name_label, 1, 0, 1, 1)
        grid.attach(self.name_entry, 1, 1, 1, 1)
        grid.attach(self.name_button, 1, 2, 1, 1)
        grid.attach(self.status_label, 1, 3, 1, 1)
        
        area.add(grid)        
        self.show_all()  
    
    def attempt_save(self, widget):
        '''Attempts to save the file in 
        the current data base'''
        file_name = self.name_entry.get_text()
        if file_name != ("" or " "):
            try:
                pass_test = self.test_file(file_name)
                if pass_test:
                    self.status_label.set_text("Name save successful")
                    self.save_file(file_name)
                    time.sleep(2)
                else:
                    self.status_label.set_text("Name Taken")
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "Override Prompt")
                    dialog.format_secondary_text(override_prompt)
                    response = dialog.run()
                    if response == Gtk.ResponseType.OK:
                        self.override_file_name(file_name)
                        self.status_label.set_text("File Name Overridden and Saved")
                    else:
                        self.status_label.set_text("Choose another name")
                    dialog.destroy()
            except Exception, e:
                print("Error during save file attempt: "+str(e))
        else:
            self.status_label.set_text("No name detected, defaulting")
            self.save_file(str(time.clock()))
            time.sleep(2)
    
    def test_file(self, file):
        '''test the file against the
        current DB of files'''
        global current_files_list
        try:
            if file in current_files_list:
                print("File name taken")
                return False
            elif file not in current_files_list:
                print("Name test passed, file name reserved")
                current_files_list.append(file)
                return True
            else:
                raise NameError("File name check failure, abort testing")
        except Exception as e:
            print("Failed To test name: "+str(e))
    
    def override_file_name(self, file):
        '''finds the file and overrides it
        essentially replaces a file'''
        pass
    
    def save_file(self, file):
        '''Creates the file and saves 
        it to the designated file directory '''
        pass
                
    