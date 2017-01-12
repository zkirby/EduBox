'''
Created on Feb 4, 2016

@author: zachary
'''
import gi, math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm
import scipy as syp
import scikits.bootstrap as bootstrap  

class StatisticsPopUp(Gtk.Dialog):
    
    def __init__(self, parent):
        global data_content, data_names
        Gtk.Dialog.__init__(self, "Statistics Workstation", parent, Gtk.DialogFlags.DESTROY_WITH_PARENT,(
            "Write Data", Gtk.ResponseType.CANCEL, 
            "Finished", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 100)
        self.set_border_width(30)
        area = self.get_content_area()   
        self.current_list = []
        self.current_list_name = ""
        data_content, data_names = load_expressions_data()
        
        #Setup Componets for Data
        grid = Gtk.Grid()
        self.stack = Gtk.Stack()
        self.stack_switcher = Gtk.StackSwitcher()
        self.list_name_label = Gtk.Label("List: ")
        self.output_label = Gtk.Label("Output")
        self.choose_label = Gtk.Label("Choose List")
        self.choose_data_dropdown = Gtk.ComboBoxText()
        self.add_new_list = Gtk.Button("New List")
        self.list_numbers = Gtk.Button("View Data")
        self.five_number_button = Gtk.Button("5# summary")
        #self.graph_histogram = Gtk.Button("Graph Histogram")
        self.result_area = Gtk.TextView()
        self.result_area_buffer = self.result_area.get_buffer()
        
        #Setup Componets For Statistics 
        grid_stat = Gtk.Grid()
        self.data_label = Gtk.Label("List: ")
        self.output_label_stat = Gtk.Label("Output")
        self.distribution_button = Gtk.Button("Normality Test") 
        self.CI_button = Gtk.Button("C.I.")
        self.t_test_button = Gtk.Button("T-Test")
        self.result_area_stat = Gtk.TextView()
        self.result_area_buffer_stat = self.result_area_stat.get_buffer()
        
        #Componet Options for Algebra
        self.result_area.set_editable(False)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)
        self.stack.add_titled(grid, "data list set", "Data")
        self.stack_switcher.set_stack(self.stack)
        
        #Componet Options for Calc
        self.result_area_stat.set_editable(False)
        self.stack.add_titled(grid_stat, "statistics eval", "Stat")
        self.make_terms_list()
        
        #Connections
        self.five_number_button.connect('clicked', self.num_5_sum)
        self.CI_button.connect('clicked', self.confidence_interval)
        self.t_test_button.connect('clicked', self.t_test_run)
        self.distribution_button.connect('clicked', self.normality)
        self.list_numbers.connect('clicked', self.view_list)
        self.add_new_list.connect('clicked', self.add_data_set)
        self.choose_data_dropdown.connect("changed", self.pick_set)
        
        #Build Grid For Data (left, top, width, height)
        grid.attach(self.list_name_label, 1, 0, 1, 1)
        grid.attach(self.choose_data_dropdown, 1, 1, 1, 1)
        grid.attach(self.add_new_list, 1, 2, 1, 1)
        grid.attach(self.list_numbers, 1, 3, 1, 1)
        grid.attach(self.five_number_button, 1, 4, 1, 1)
        #grid.attach(self.graph_histogram, 1, 5, 1, 1)
        grid.attach(self.result_area, 4, 1, 1, 1)
        grid.attach(self.output_label, 4, 0, 1, 1)
        
        #Build Grid For Statistics (left, top, width, height)
        grid_stat.attach(self.data_label, 1, 0, 1, 1)
        grid_stat.attach(self.distribution_button, 1, 1, 1, 1)
        grid_stat.attach(self.CI_button, 1, 2, 1, 1)
        grid_stat.attach(self.t_test_button, 1, 3, 1, 1)
        grid_stat.attach(self.result_area_stat, 4, 1, 1, 1)
        grid_stat.attach(self.output_label_stat, 4, 0, 1, 1)
        
        area.add(self.stack_switcher)
        area.add(self.stack)        
        self.show_all()  
        
    def make_terms_list(self):
        global data_names
        self.choose_data_dropdown.remove_all()
        for i,name in enumerate(data_names):
            self.choose_data_dropdown.insert(i+1, str(i+1), name)
    
    def view_list(self, widget):
        '''view all the data points
        of the current list'''
        num_list = self.current_list
        try:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, self.current_list_name)
            dialog.format_secondary_text(str(num_list))
            dialog.run()
            dialog.destroy()
            print("Data View Dialog Terminated")
        except Exception, e:
            print("Error viewing data list: "+str(e))
    
    def num_5_sum(self, widget):
        '''Obtain the mean, medium, mode,
        stand dev, and variance of a given list'''
        num_list = self.current_list
        try:
            nums, mi, mea, var, sk, ku = stats.describe(num_list)
            std = math.sqrt(var)
            to_write = ("5 Number summary:\nMean: %s, Variance: %s, Max/min: %s, Standard Deviation: %s, Skewdeness: %s") %(mea, var, mi, std, sk)
            self.result_area_buffer.set_text(to_write)
        except Exception, e:
            print("Error Processing 5 Number Summary: "+str(e))
        
    def confidence_interval(self, widget):
        '''Obtain the confidence interval of a 
        data set from num_list'''
        num_list = self.current_list
        try:
            C_I = bootstrap.ci(data=num_list, statfunction=syp.mean, alpha=0.05)  
            write_to = "The Confidence Interval For this data is:\n (%s, %s)" %(str(C_I[0]),str(C_I[1]))
            self.result_area_buffer_stat.set_text(write_to)
        except Exception, e:
            print("Error Grabbing Confidence Interval: "+str(e))
        
    def t_test_run(self, widget):
        '''Runs a basic T_test for 
        the given list'''
        num_list = self.current_list
        try:
            t_results, p_result = stats.ttest_1samp(num_list, norm.mean())
            to_write = "The T_Test for the List Returned:\nt-value: "+str(t_results)+" p-value: "+str(p_result)
            self.result_area_buffer_stat.set_text(to_write)
        except Exception, e:
            print("Error Finding T-test: "+str(e))
    
    def normality(self, widget):
        '''Runs a normality test
        on the given list'''
        num_list = self.current_list
        try:
            normal = stats.normaltest(num_list)
            write_to = "The Normality Test Returned:\n normaltest teststat: %s, p-value: %s" %(normal[0], normal[1])
            self.result_area_buffer_stat.set_text(write_to)
        except Exception, e:
            print("Error finding normality: "+str(e))
    
    def add_data_set(self, widget):
        global data_names, data_content
        dialog = AddData(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.CANCEL:
            print("No Data Added")
            
        elif response == Gtk.ResponseType.OK:
            try:
                print("List: "+dialog.input_funct_name.get_text()+" Added")
                data_names.append(dialog.input_funct_name.get_text())
                start, end = dialog.input_funct_buffer.get_bounds()
                try: 
                    item = map(int, dialog.input_funct_buffer.get_text(start, end, False).split())
                except Exception, e:
                    print("Data set was invalid: "+str(e))
                    self.result_area_buffer.set_text("Data set was not added. Make sure you entered numbers only!")
                    item = [0,1]; data_names[-1] = "INVALID LIST"
                data_content.append(item)
                self.make_terms_list()
            except Exception, e:
                print("Failed to Add new List: "+str(e))

        dialog.destroy()
    
    def pick_set(self, widget):
        '''Picks from the dropdown menu
        allows the user to select a list entry'''
        global data_names, data_content
        
        self.current_list_name = self.choose_data_dropdown.get_active_text()
        if self.current_list_name != None:
            list_content = data_names.index(self.current_list_name)
            self.list_name_label.set_text(self.current_list_name); self.data_label.set_text(self.current_list_name)
        else:
            list_content = 0
            self.list_name_label.set_text("List: "); self.data_label.set_text("List: ")
        this_list = data_content[list_content]
        self.current_list = this_list
        print(self.current_list, self.current_list_name)

class AddData(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add a Data List", parent, Gtk.DialogFlags.MODAL, (
            "Cancel", Gtk.ResponseType.CANCEL, 
            "Add Data", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 400)
        self.set_border_width(30)
        area = self.get_content_area()
        
        #Add Componets
        self.input_label = Gtk.Label("List Name")
        self.input_labe_func = Gtk.Label("Data")
        self.input_funct_name = Gtk.Entry()
        self.input_funct = Gtk.TextView() 
        self.input_funct_buffer = self.input_funct.get_buffer()
        
        area.add(self.input_label)
        area.add(self.input_funct_name)
        area.add(self.input_labe_func)
        area.add(self.input_funct)        
        self.show_all() 
            
def load_expressions_data():
    '''Loads all the previously saved
    expressions of the user'''
    data_list = []
    names_list = [] 
    
    #Open Files
    try:
        data_file = open('Resources/Statistics Files/data_lists', 'r')
    except Exception, e:
        print("Failure Opening List data: "+e)
    
    #Put Content Together
    for i,funct in enumerate(data_file):
        if i%2 == 0:
            names_list.append(funct[:-1])
        else:
            to_put = map(int, funct.split())
            data_list.append(to_put)
            
    print(data_list)
    print(names_list)
    #Close Files
    try:
        data_file.close()
    except Exception, e:
        print("Faliure closing Data Files: "+str(e))
    
    return data_list, names_list

def stats_popup_finished():
    '''Writes the functions back 
    into the file to save it'''
    global data_content, data_names
    
    #Open Files
    try:
        data_file = open('Resources/Statistics Files/data_lists', 'w')
    except Exception, e:
        print("Failure Opening Functions data to save: "+e)
        
    for i,item in enumerate(data_content):
        if data_names[i] != "INVALID LIST":
            data_file.write(str(data_names[i])+"\n")
            temp_name = ""
            for pen in item:
                if type(pen) == type(2):
                    temp_name+=(str(pen) + " ")
            data_file.write(temp_name+"\n")
    
    try:
        data_file.close()
    except Exception, e:
        print("Faliure closing Data Files: "+str(e))


    

        