'''
Created on Feb 4, 2016

@author: zachary
'''
import gi, math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sympy as sy
from sympy import Poly
import matplotlib.pyplot as plt

class MathPopUp(Gtk.Dialog):
    
    def __init__(self, parent):
        global func_data_list
        Gtk.Dialog.__init__(self, "Mathamatics Workstation", parent, Gtk.DialogFlags.MODAL, (
            "Write Data", Gtk.ResponseType.CANCEL, 
            "Finished", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 100)
        self.set_border_width(30)
        area = self.get_content_area()   
        func_data_list = load_expressions_data()
        sy.init_printing(use_unicode=True)

        #Setup Componets for Algebra
        grid = Gtk.Grid()
        self.stack = Gtk.Stack()
        self.stack_switcher = Gtk.StackSwitcher()
        self.input_label = Gtk.Label("Input Expression")
        self.output_label = Gtk.Label("Output")
        self.input_entry = Gtk.Entry()
        self.factor_button = Gtk.Button("Factor")
        self.save_expressions_button = Gtk.Button("Save Function")
        self.list_expressions = Gtk.Button("My Functions")
        self.graph_button = Gtk.Button("Graph")
        self.result_area = Gtk.TextView()
        self.result_area_buffer = self.result_area.get_buffer()
        
        #Setup Componets For Calc
        grid_calc = Gtk.Grid()
        self.input_label_calc = Gtk.Label("Input Expression")
        self.output_label_calc = Gtk.Label("Output")
        self.input_entry_calc = Gtk.Entry()
        self.limit_button = Gtk.Button("Limit")
        self.derive_button = Gtk.Button("Derive")
        self.integrate_button = Gtk.Button("Integrate")
        self.series_button = Gtk.Button("Series")
        self.result_area_calc = Gtk.TextView()
        self.result_area_buffer_calc = self.result_area_calc.get_buffer()
        
        #Componet Options for Algebra
        self.result_area.set_editable(False)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        self.stack.add_titled(grid, "alebraic expressions", "Algebra")
        self.stack_switcher.set_stack(self.stack)
        
        #Componet Options for Calc
        self.result_area_calc.set_editable(False)
        self.stack.add_titled(grid_calc, "claculus equations", "Calculus")
        
        #Connections
        self.factor_button.connect("clicked", self.factor_value)
        self.save_expressions_button.connect("clicked", self.save_current_expression)
        self.list_expressions.connect("clicked", self.list_saved_expressions)
        self.graph_button.connect("clicked", self.graph_expression, range(-10, 10))
        self.derive_button.connect("clicked", self.derive_function)
        self.integrate_button.connect("clicked", self.intergrate_function)
        self.limit_button.connect("clicked", self.limit_to_zero)
        self.series_button.connect("clicked", self.series_of_function)
        
        #Build Grid For Algebra (left, top, width, height)
        grid.attach(self.input_label, 1, 0, 1, 1)
        grid.attach(self.input_entry, 1, 1, 1, 1)
        grid.attach(self.factor_button, 1, 2, 1, 1)
        grid.attach(self.list_expressions, 1, 3, 1, 1)
        grid.attach(self.save_expressions_button, 1, 4, 1, 1)
        grid.attach(self.graph_button, 1, 5, 1, 1)
        grid.attach(self.result_area, 4, 1, 1, 1)
        grid.attach(self.output_label, 4, 0, 1, 1)
        
        #Build Grid For Calc (left, top, width, height)
        grid_calc.attach(self.input_label_calc, 1, 0, 1, 1)
        grid_calc.attach(self.input_entry_calc, 1, 1, 1, 1)
        grid_calc.attach(self.limit_button, 1, 2, 1, 1)
        grid_calc.attach(self.derive_button, 1, 3, 1, 1)
        grid_calc.attach(self.integrate_button, 1, 4, 1, 1)
        grid_calc.attach(self.series_button, 1, 5, 1, 1)
        grid_calc.attach(self.result_area_calc, 4, 1, 1, 1)
        grid_calc.attach(self.output_label_calc, 4, 0, 1, 1)
        
        area.add(self.stack_switcher)
        area.add(self.stack)        
        self.show_all()  
        
    def derive_function(self, widget):
        try:
            x = sy.symbols('x')
            current_expression = str(self.input_entry_calc.get_text().lower())
            text_item = "The Derivative of "+str(current_expression)+" is:\n"
            expre_to_eval = sy.sympify(current_expression)
            to_write = str(sy.diff(expre_to_eval, x))
            if to_write.count("Derivative") > 0: 
                raise NameError("Can't be Derived")
            else:
                self.result_area_buffer_calc.set_text(text_item+to_write)
        except Exception, e:
            print("Falure to Derive Expression: "+str(e))
            self.result_area_buffer_calc.set_text("I'm Sorry, that expression\n Can't be Derived, make sure you\n typed everything correctly ")

    def intergrate_function(self, widget):
        try:
            x = sy.symbols('x')
            current_expression = str(self.input_entry_calc.get_text().lower())
            text_item = "The Integral of "+str(current_expression)+" is:\n"
            expre_to_eval = sy.sympify(current_expression)
            to_write = str(sy.integrate(expre_to_eval, x))
            if to_write.count("Integral") > 0:
                raise NameError("Can't be Integrated")
            else:
                self.result_area_buffer_calc.set_text(text_item+"("+to_write+")+C")
        except Exception, e:
            print("Falure to Integrate Expression: "+str(e))
            self.result_area_buffer_calc.set_text("I'm Sorry, that expression\n Can't be Integrated, make sure you\n typed everything correctly ")
            
    def limit_to_zero(self, widget):
        try:
            x = sy.symbols('x')
            current_expression = str(self.input_entry_calc.get_text().lower())
            text_item = "The Limit of "+str(current_expression)+" as X approches Zero is:\n"
            expre_to_eval = sy.sympify(current_expression)
            to_write = str(sy.limit(expre_to_eval, x, 0))
            if to_write.count("Limit") > 0:
                raise NameError("Can't Find Limit")
            else:
                self.result_area_buffer_calc.set_text(text_item+to_write)
        except Exception, e:
            print("Falure to Find Limit: "+str(e))
            self.result_area_buffer_calc.set_text("I'm Sorry, that expression\n has no Limit at 0, make sure you\n typed everything correctly ")
            
    def series_of_function(self, widget):
        try:
            x = sy.symbols('x')
            current_expression = str(self.input_entry_calc.get_text().lower())
            text_item = "The Maclurin Series of "+str(current_expression)+" is:\n"
            expre_to_eval = sy.sympify(current_expression)
            to_write = str(expre_to_eval.series(x, 0, 4).removeO())
            self.result_area_buffer_calc.set_text(text_item+to_write)
        except Exception, e:
            print("Falure to Find Series: "+str(e))
            self.result_area_buffer_calc.set_text("I'm Sorry, that expression\n can't be made into a series, make sure you\n typed everything correctly ")
          
            
    def save_current_expression(self, widget):
        global func_data_list
        dialog = AddFunction(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.CANCEL:
            print("No Function Selected")
            
        elif response == Gtk.ResponseType.OK:
            print("Function: "+dialog.input_funct_name.get_text()+" Added")
            new_list_item = [dialog.input_funct_name.get_text(), dialog.input_funct.get_text()]
            func_data_list.append(new_list_item)
            
        dialog.destroy()
    
    def list_saved_expressions(self, widget):
        global selected_function
        dialog = SelectFunction(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.CANCEL:
            print("No Function Selected")
            
        elif response == Gtk.ResponseType.OK:
            print("Function: "+selected_function+" Chosen")
            self.input_entry.set_text(selected_function)
            self.input_entry_calc.set_text(selected_function)
            
        dialog.destroy()
          
    
    def factor_value(self, widget):
        try:
            current_expression = str(self.input_entry.get_text().lower())
            text_item = "Factors of "+str(current_expression)+" are:\n"
            expre_to_eval = sy.sympify(current_expression)
            to_write = Poly(expre_to_eval).all_roots()
            items_list = []
            for item in to_write:
                if item not in items_list:
                    text_item+=str(item)+"\n"
                    items_list.append(item)
            self.result_area_buffer.set_text(text_item)
        except Exception, e:
            print("Falure to Factor Expression: "+str(e))
            self.result_area_buffer.set_text("I'm Sorry, that expression\n Can't be Factored, make sure you\n typed everything correctly ")

    def graph_expression(self, widget, points):
        try:
            x = sy.symbols('x')
            current_expression = str(self.input_entry.get_text().lower())
            expre_to_eval = sy.sympify(current_expression)
            x_points = []; y_points = []
            for i in points:
                x_points.append(i); y_points.append(expre_to_eval.subs(x,i))
            plt.plot(x_points, y_points, 'bo', linestyle='-')
            plt.show()
        except Exception, e:
            print("Failed To Graph data: "+str(e))
            self.result_area_buffer.set_text("I'm Sorry, that expression\n Can't be Graphed, make sure you\n typed everything correctly ")

class SelectFunction(Gtk.Dialog):
    
    def __init__(self, parent):
        global selected_function, func_data_list
        Gtk.Dialog.__init__(self, "Select A Function", parent, Gtk.DialogFlags.MODAL, (
            "Cancel", Gtk.ResponseType.CANCEL, 
            "Select Function", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 400)
        self.set_border_width(30)
        area = self.get_content_area()
        selected_function = ""
        
        #Add Componets
        self.function_list_storage = add_componets(func_data_list)
        self.treeview = Gtk.TreeView(model=self.function_list_storage)
        self.renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Name", self.renderer_text, text=0)
        column_text.set_sort_column_id(0)
        self.treeview.append_column(column_text)
        column_text_next = Gtk.TreeViewColumn("Function", self.renderer_text, text=1)
        column_text_next.set_sort_column_id(1)
        self.treeview.append_column(column_text_next)

        selected_row = self.treeview.get_selection()
        selected_row.connect("changed", self.item_selected)
        
        area.add(self.treeview)        
        self.show_all() 
    
    def item_selected(self, selection):
        global selected_function
        model, row = selection.get_selected()
        if row is not None:
            selected_function = model[row][1]

class AddFunction(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Select A Function", parent, Gtk.DialogFlags.MODAL, (
            "Cancel", Gtk.ResponseType.CANCEL, 
            "Add Function", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 400)
        self.set_border_width(30)
        area = self.get_content_area()
        
        #Add Componets
        self.input_label = Gtk.Label("Function Name")
        self.input_labe_func = Gtk.Label("Function")
        self.input_funct_name = Gtk.Entry()
        self.input_funct = Gtk.Entry() 
        
        area.add(self.input_label)
        area.add(self.input_funct_name)
        area.add(self.input_labe_func)
        area.add(self.input_funct)        
        self.show_all() 
            
def load_expressions_data():
    '''Loads all the previously saved
    expressions of the user'''
    functions_list = [[]]
    list_count = 0
    
    #Open Files
    try:
        function_file = open('Resources/Math Files/functions_database', 'r')
    except Exception, e:
        print("Failure Opening Functions data: "+e)
    
    #Put Content Together
    for i,funct in enumerate(function_file):
        if i%2 == 0 and i != 0:
            functions_list.append([])
            list_count+=1
        functions_list[list_count].append(str(funct[:-1]))
    
    #Close Files
    try:
        function_file.close()
    except Exception, e:
        print("Faliure closing Function Files: "+str(e))
    
    print(functions_list)
    return functions_list

def math_popup_finished():
    '''Writes the functions back 
    into the file to save it'''
    global func_data_list
    
    #Open Files
    try:
        function_file = open('Resources/Math Files/functions_database', 'w')
    except Exception, e:
        print("Failure Opening Functions data to save: "+e)
        
    for item in func_data_list:
        for func in item:
            function_file.write(str(func)+"\n")
    
    try:
        function_file.close()
    except Exception, e:
        print("Faliure closing Function Files: "+str(e))

def add_componets(lists):
    '''adds items to a tree 
    view and creates a stroage space'''
    storage = Gtk.ListStore(str, str)
    try:
        for item in lists:
            storage.append(item)
    except Exception, e:
        print("Falure adding items to the TreeView: "+str(e))
    
    return storage
    
    

        