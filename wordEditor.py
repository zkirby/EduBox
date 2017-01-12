'''
Created on Jan 11, 2016

@author: zachary
'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Pango, Gdk
import componets
import Popup as pu
from Popup import english_popup, history_popup
#import locale
#from gtkspellcheck import SpellChecker

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileNew' />
      <menuitem action='FileOpen' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditUndo' />
      <menuitem action='EditUndoAll' />
    </menu>
    <menu action='StyleMenu'>
      <menuitem action='StyleFontUp' />
      <menuitem action='StyleFontDown' />
      <separator />
      <menuitem action='StyleItalic' />
      <menuitem action='StyleBold' />
      <menuitem action='StyleUnderline' />
    </menu>
    <menu action='ClassesMenu'>
      <menuitem action='ClassesMath' />
      <menuitem action='ClassesStatistics' />
      <menuitem action='ClassesPhysics' />
      <menuitem action='ClassesEnglish' />
      <menuitem action='ClassesHistory' />
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='HelpAbout' />
      <menuitem action='HelpMechanics' />
      <menuitem action='HelpCredits' />
    </menu>
  </menubar>
</ui>
"""
class MainWindow(Gtk.Window):
    
    def __init__(self):            
            Gtk.Window.__init__(self, title="~~Note Taker Editor~~")
            self.set_default_size(400, 400)
            self.set_border_width(10)
            self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            self.add(self.box)
            
            self.tool_bar = componets.BuildToolBar()
            self.text_view = componets.BuildTextView()
            self.textbuffer = self.text_view.area_buffer
#             self.spellChecker = SpellChecker(self.text_view.area, locale.getdefaultlocale()[0])
#             self.spellChecker.enable()
            
            action_group = Gtk.ActionGroup("my_actions")
            
            self.create_tags(self.text_view)
            self.create_button_group(self.tool_bar, self.text_view)
            
            self.add_file_menu_actions(action_group)
            self.add_edit_menu_actions(action_group)
            self.add_style_menu_actions(action_group)
            self.add_classes_menu_actions(action_group)
            self.add_help_menu_actions(action_group)
       
            uimanager = self.create_ui_manager()
            uimanager.insert_action_group(action_group)

            self.main_menu_bar = uimanager.get_widget("/MenuBar")
            self.box.pack_start(self.main_menu_bar, False, False, 0)

            self.tool_bar.build_self(self.box)    
            self.text_view.build_self(self.box)
            self.about_c, self.mechanics_c, self.credits_c = pu.popup_build()
            
    def create_button_group(self, tools, tag_from):
        tools.font_up_button.connect("clicked", self.edit_feature, tag_from.tag_size)
        tools.font_down_button.connect("clicked", self.edit_feature, tag_from.tag_size3)
        tools.font_clear_button.connect("clicked", self.edit_feature, tag_from.tag_size2)
        tools.highlight_button.connect("clicked", self.edit_feature, tag_from.tag_found)
        tools.bold_button.connect("clicked", self.edit_feature, tag_from.tag_bold)
        tools.italics_button.connect("clicked", self.edit_feature, tag_from.tag_italic)
        tools.underline_button.connect("clicked", self.edit_feature, tag_from.tag_underline)
        tools.justify_right_button.connect("clicked", self.justify_action, Gtk.Justification.RIGHT)
        tools.justify_left_button.connect("clicked", self.justify_action, Gtk.Justification.LEFT)
        tools.justify_center_button.connect("clicked", self.justify_action, Gtk.Justification.CENTER)
        tools.clear_button.connect("clicked", self.on_undo)
        
    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(UI_INFO)
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager
        
    def create_tags(self, tag_from):
        tag_from.tag_bold = tag_from.area_buffer.create_tag("bold", weight=Pango.Weight.BOLD)
        tag_from.tag_italic = tag_from.area_buffer.create_tag("italic", style=Pango.Style.ITALIC)
        tag_from.tag_underline = tag_from.area_buffer.create_tag("underline", underline=Pango.Underline.SINGLE)
        tag_from.tag_found = tag_from.area_buffer.create_tag("found", background="yellow")
        tag_from.tag_size = tag_from.area_buffer.create_tag("size", size=20000)
        tag_from.tag_size2 = tag_from.area_buffer.create_tag("size 2", size=10000)
        tag_from.tag_size3 = tag_from.area_buffer.create_tag("size 3", size=5000)
            
    def justify_action(self, button, justify):
        self.text_view.area.set_justification(justify)
               
    def edit_feature(self, widget, tag):
        bounds = self.text_view.area_buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.text_view.area_buffer.apply_tag(tag, start, end)
        
    def on_clear_clicked(self, widget):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)    
        
    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_new = Gtk.Action("FileNew", "_New", "Create a new file", "New...")
        action_new.connect("activate", self.on_new_file)
        action_group.add_action_with_accel(action_new, None)

        action_open = Gtk.Action("FileOpen", "_Open", "Open a File", "Open", "<control>A")
        action_open.connect("activate", self.on_open_file)
        action_group.add_action(action_open)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)
        
    def add_edit_menu_actions(self, action_group):
        
        action_group.add_actions([
            ("EditMenu", None, "Edit"),
            ("EditUndo", None, "Undo", "<control>Z", None, self.on_undo),
            ("EditUndoAll", None, "Undo All", "<control><alt>Z", None, self.on_undo_all)
        ])
        
    def add_style_menu_actions(self, action_group):
        
        action_group.add_actions([
            ("StyleMenu", None, "Style"),
            ("StyleFontUp", None, "Font Up", None, None, self.font_up),
            ("StyleFontDown", None, "Font Down", None, None, self.font_down),
            ("StyleItalic", None, "Italics", "<control>I", None, self.font_italic),
            ("StyleBold", None, "Bold", "<control>B", None, self.font_bold),
            ("StyleUnderline", None, "Underline", "<control>U", None, self.font_underline)
        ])

    def add_classes_menu_actions(self, action_group):
        
        action_group.add_actions([
            ("ClassesMenu", None, "Classes"),
            ("ClassesMath", None, "Math", "<control>M", None, self.math_popup),
            ("ClassesStatistics", None, "Statistics", "<control>S", None, self.math_popup),
            ("ClassesPhysics", None, "Physics", "<control>P", None, self.math_popup),
            ("ClassesEnglish", None, "English", "<control>E", None, self.english_popup),
            ("ClassesHistory", None, "History" ,"<control>H", None, self.history_popup)
        ])
        
    def add_help_menu_actions(self, action_group):
        
        action_group.add_actions([
            ("HelpMenu", None, "help"),
            ("HelpAbout", None, "About", None, None, self.on_about_clicked),
            ("HelpMechanics", None, "Mechanics", None, None, self.on_mechanics_clicked),
            ("HelpCredits", None, "Credits", None, None, self.on_credits_clicked)          
        ])
        
    def math_popup(self, widget):
        print("Math")
    
    def english_popup(self, widget):
        dialog = english_popup.EnglishPopUp(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            print("English Popup Closed")
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Data Written")
            start, end = dialog.result_area_buffer.get_bounds()
            start_here, end_here = self.textbuffer.get_bounds()
            to_content = dialog.result_area_buffer.get_text(start, end, False)
            self.textbuffer.set_text(self.textbuffer.get_text(start_here, end_here, False) + "\n" +to_content)
        
        dialog.destroy()
    
    def history_popup(self, widget):
        dialog = history_popup.HistoryPopUp(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            print("History Popup Closed")
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Data Written")
            start, end = dialog.view_area_buffer.get_bounds()
            start_here, end_here = self.textbuffer.get_bounds()
            to_name = dialog.term_entry.get_text()
            to_content = dialog.view_area_buffer.get_text(start, end, False)
            to_write = to_name+": "+to_content
            self.textbuffer.set_text(self.textbuffer.get_text(start_here, end_here, False) + "\n" +to_write)
            
        
        history_popup.history_popup_finished()
        dialog.destroy()
    
    def on_new_file(self, widget):
        print("New File Created")
        
    def on_open_file(self, widget):
        print("Opening a file")
    
    def on_menu_file_quit(self, widget):
        Gtk.main_quit()
        
    def on_about_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "About")
        dialog.format_secondary_text(self.about_c)
        dialog.run()
        dialog.destroy()
        print("About Dialog Terminated")
    
    def on_mechanics_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "How it Works")
        dialog.format_secondary_text(self.mechanics_c)
        dialog.run()
        dialog.destroy()
        print("Mechanics Dialog Terminated")
        
    def on_credits_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "Credits")
        dialog.format_secondary_text(self.credits_c)
        dialog.run()
        dialog.destroy()
        print("Credits Dialog Terminated")
    
    def on_undo(self, widget):
        bounds = self.text_view.area_buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.text_view.area_buffer.remove_all_tags(start, end)
    
    def on_undo_all(self, widget):
        start = self.text_view.area_buffer.get_start_iter()
        end = self.text_view.area_buffer.get_end_iter()
        self.text_view.area_buffer.remove_all_tags(start, end)
        
    def font_up(self, widget):
        bounds = self.text_view.area_buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.text_view.area_buffer.apply_tag(self.text_view.tag_size, start, end)
    
    def font_down(self, widget):
        bounds = self.text_view.area_buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.text_view.area_buffer.apply_tag(self.text_view.tag_size3, start, end)
            
    def font_italic(self, widget):
        bounds = self.text_view.area_buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.text_view.area_buffer.apply_tag(self.text_view.tag_italic, start, end)    
        
    def font_bold(self, widget):
        bounds = self.text_view.area_buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.text_view.area_buffer.apply_tag(self.text_view.tag_bold, start, end)
            
    def font_underline(self, widget):
        bounds = self.text_view.area_buffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.text_view.area_buffer.apply_tag(self.text_view.tag_underline, start, end)

#Run Main Loop and Code
windo = MainWindow()
windo.connect("delete-event", Gtk.main_quit)
windo.show_all()
Gtk.main()