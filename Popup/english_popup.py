'''
Created on Feb 4, 2016

@author: zachary
'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from network_tools import definition_parser as dp

class EnglishPopUp(Gtk.Dialog):
    
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "English Workstation", parent, Gtk.DialogFlags.MODAL, (
            "Write Data", Gtk.ResponseType.CANCEL, 
            "Finished", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 100)
        self.set_border_width(30)
        area = self.get_content_area()

        #Setup Componets
        grid = Gtk.Grid()
        self.word_label = Gtk.Label("Enter Word")
        self.word_result_label = Gtk.Label("Result")
        self.word_entry = Gtk.Entry()
        self.spell_check_button = Gtk.Button("Check Spelling")
        self.syn_button = Gtk.Button("Synonyms")
        self.define_button = Gtk.Button("Define")
        self.mla_button = Gtk.Button("Format MLA")
        self.result_area = Gtk.TextView()
        self.result_area_buffer = self.result_area.get_buffer()
        
        #Componet Options
        self.result_area.set_editable(True)
        
        #Connections
        self.define_button.connect("clicked", self.define_word)
        self.spell_check_button.connect("clicked", self.spell_check)
        
        #Build Grid (left, top, width, height)
        grid.attach(self.word_label, 1, 0, 1, 1)
        grid.attach(self.word_entry, 1, 1, 1, 1)
        grid.attach(self.spell_check_button, 1, 2, 1, 1)
        grid.attach(self.syn_button, 1, 3, 1, 1)
        grid.attach(self.define_button, 1, 4, 1, 1)
        grid.attach(self.mla_button, 1, 5, 1, 1)
        grid.attach(self.result_area, 4, 1, 1, 1)
        grid.attach(self.word_result_label, 4, 0, 1, 1)
        
        
        area.add(grid)        
        self.show_all()        
        
    def define_word(self, widget):
        try:
            to_write = ""
            word = self.word_entry.get_text()
            define = dp.definition_search(word)
            for item in define:
                to_write+=item+"\n"
            self.result_area_buffer.set_text(to_write)
        except Exception, e:
            print("Failed TO define given word")
    
    def spell_check(self, widget):
        to_check = ""
        word = self.word_entry.get_text()
        
        self.result_area_buffer.set_text(to_check)