'''
Created on Jan 16, 2016

@author: zachary
'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Pango

class BuildTextView:
    
    def __init__(self):
        self.area = Gtk.TextView()
        self.area_buffer = self.area.get_buffer()
        self.area.set_wrap_mode(Gtk.WrapMode.WORD)
    
    def build_self(self, cont):
        cont.pack_start(self.area, True, True, 0)
    
class BuildToolBar:
    
    def __init__(self):    
        self.header_bar = Gtk.Toolbar()
        
        #Button Instances 
        self.font_up_button = Gtk.ToolButton(); self.font_clear_button = Gtk.ToolButton(); self.font_down_button = Gtk.ToolButton()
        self.justify_right_button = Gtk.ToolButton(); self.justify_center_button = Gtk.ToolButton(); self.justify_left_button = Gtk.ToolButton()
        self.bold_button = Gtk.ToolButton(); self.italics_button = Gtk.ToolButton(); self. underline_button = Gtk.ToolButton()
        self.highlight_button = Gtk.ToolButton(); self.clear_button = Gtk.ToolButton()
    
        #Create Buttons
        self.create_button(self.font_up_button, "go-up-symbolic", 0)
        self.create_button(self.font_clear_button, "edit-undo-symbolic", 1)
        self.create_button(self.font_down_button, "go-down-symbolic", 2)
        self.header_bar.insert(Gtk.SeparatorToolItem(), 3)
        self.create_button(self.justify_left_button, "format-justify-left-symbolic", 4)
        self.create_button(self.justify_center_button, "format-justify-center-symbolic", 5)
        self.create_button(self.justify_right_button, "format-justify-right-symbolic", 6)
        self.header_bar.insert(Gtk.SeparatorToolItem(), 7)
        self.create_button(self.bold_button, "format-text-bold-symbolic", 8)
        self.create_button(self.italics_button, "format-text-italic-symbolic", 9)
        self.create_button(self.underline_button, "format-text-underline-symbolic", 10)
        self.header_bar.insert(Gtk.SeparatorToolItem(), 11)
        self.create_button(self.highlight_button, "face-smile-symbolic", 12)
        self.create_button(self.clear_button, "edit-clear-symbolic", 13)
        
    def create_button(self, name, icon_name, pos):
        name.set_icon_name(icon_name)
        self.header_bar.insert(name, pos)
        
    def build_self(self, cont):
        cont.pack_start(self.header_bar, False, False, 0)
        
        


