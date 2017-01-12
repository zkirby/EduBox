'''
Created on Feb 4, 2016

@author: zachary
'''
import gi, math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sympy as sy
import matplotlib.pyplot as plt

class PhysicsPopUp(Gtk.Dialog):
    
    def __init__(self, parent):
        global data_content, data_names
        Gtk.Dialog.__init__(self, "Physics Workstation", parent, Gtk.DialogFlags.DESTROY_WITH_PARENT,(
            "Write Data", Gtk.ResponseType.CANCEL, 
            "Finished", Gtk.ResponseType.OK))
        
        self.set_default_size(200, 100)
        self.set_border_width(30)
        area = self.get_content_area()   
        
        #Setup Componets
        grid = Gtk.Grid()
        self.distance_label = Gtk.Label("Distance")
        self.distance_entry = Gtk.Entry()
        self.velocity_label = Gtk.Label("Velocity")
        self.velocity_entry = Gtk.Entry()
        self.acceleration_label = Gtk.Label("Acceleration")
        self.acceleration_entry = Gtk.Entry()
        self.graph_distance = Gtk.Button("d(t) Graph")
        self.graph_velocity = Gtk.Button("v(t) Graph")
        self.graph_acceleration = Gtk.Button("a(t) Graph")
        self.converter_button = Gtk.Button("Converter")
        self.result_area = Gtk.TextView()
        self.result_area_buffer = self.result_area.get_buffer()
        
        #Componet Options 
        self.result_area.set_editable(False)
    
        #Connections
        self.graph_distance.connect('clicked', self.distance_graph)
        self.graph_velocity.connect('clicked', self.velocity_graph)
        self.graph_acceleration.connect('clicked', self.acceleration_graph)
        
        #Build Grid For Data (left, top, width, height)
        grid.attach(self.distance_label, 1, 0, 1, 1)
        grid.attach(self.distance_entry, 1, 1, 1, 1)
        grid.attach(self.velocity_label, 1, 2, 1, 1)
        grid.attach(self.velocity_entry, 1, 3, 1, 1)
        grid.attach(self.acceleration_label, 1, 4, 1, 1)
        grid.attach(self.acceleration_entry, 1, 5, 1, 1)
        grid.attach(self.graph_distance, 1, 6, 1, 1)
        grid.attach(self.graph_velocity, 1, 7, 1, 1)
        grid.attach(self.graph_acceleration, 1, 8, 1, 1)
        grid.attach(self.converter_button, 1, 9, 1, 1)
        grid.attach(self.result_area, 1, 10, 1, 1)
        
        area.add(grid)        
        self.show_all()  
    
    def acceleration_graph(self, widget):
        '''Graph a linear version of
        the distance graph'''
        try:
            acceler = int(self.acceleration_entry.get_text())
        except ValueError:
            print("Acceleration must be a number with no units!"); acceler = 0
            self.result_area_buffer.set_text("Make sure your Acceleration is a unitless number")
        try:
            x_points = []; y_points = []
            for i in range(50):
                x_points.append(i); y_points.append(acceler)
            plt.plot(x_points, y_points, linestyle='-'); plt.xlabel("Time(s)"); plt.ylabel("Acceleration(m/s^2)"); plt.show()
        except Exception, e:
            print("Failed To Graph data: "+str(e))
            self.result_area_buffer.set_text("I'm Sorry, acceleration\n Can't be Graphed, make sure you\n typed everything correctly ")
            
    def velocity_graph(self, widget):
        '''Graph a velocity versus
        time graph given data'''
        self.entry_sweeper()
        veloc_on = False; veloc_sub_off = False
        if self.velocity_entry.get_text() != ("" or " "):
            try:
                veloc = int(self.velocity_entry.get_text()); veloc_on = True
            except ValueError:
                print("Velocity must be a number with no units!"); veloc = 0
                self.result_area_buffer.set_text("Make sure your Velocity is a unitless number")
        try:
            x = sy.symbols('x')
            if veloc_on:
                if self.acceleration_entry.get_text() == ("" or " "):
                    velocity_expre = veloc; veloc_sub_off = True
                elif self.acceleration_entry.get_text() != ("" or " "):
                    velocity_expre = sy.sympify(str(veloc)+"*"+'x')
            elif veloc_on == False:
                if self.acceleration_entry.get_text() == ("" or " "):
                    velocity_expre = 0; raise ValueError("No Value Given For Velocity")
                elif self.acceleration_entry.get_text() != ("" or " "):
                    velocity_expre = sy.sympify(self.acceleration_entry.get_text()+"*"+'x')
            x_points = []; y_points = []
            for i in range(50):
                if veloc_sub_off:
                    x_points.append(i); y_points.append(velocity_expre)
                elif veloc_sub_off == False:
                    x_points.append(i); y_points.append(velocity_expre.subs(x, i))
            plt.plot(x_points, y_points, linestyle='-'); plt.xlabel("Time(s)"); plt.ylabel("Velocity(m/s)"); plt.show()
        except Exception, e:
            print("Failed To Graph data: "+str(e))
            self.result_area_buffer.set_text("I'm Sorry, velocity\n Can't be Graphed, make sure you\n typed everything correctly ")

    def distance_graph(self, widget):
        '''Graph a distance versus
        time graph given data'''
        self.entry_sweeper()
        dis_on = False; dis_sub_off = False
        if self.distance_entry.get_text() != ("" or " "):
            try:
                distance = int(self.distance_entry.get_text()); dis_on = True
            except ValueError:
                print("Distance must be a number with no units!")
                self.result_area_buffer.set_text("Make sure your Distance is a unitless number")
        try:
            x = sy.symbols('x')
            acceler = self.acceleration_entry.get_text(); veloc = self.velocity_entry.get_text()
            if dis_on:
                if (acceler and veloc) == ("" or " "):
                    distance_expre = distance; dis_sub_off = True
                elif veloc != ("" or " ") and acceler == ("" or " "):
                    distance_expre = sy.sympify(veloc+"*"+"x"+"+"+str(distance))
                elif veloc != ("" or " ") and acceler != ("" or " "):
                    distance_expre = sy.sympify(str(int(acceler)/2)+"*"+"x**2"+"+"+veloc+"*"+"x"+"+"+str(distance))
                elif veloc == ("" or " ") and acceler != ("" or " "):
                    distance_expre = sy.sympify(str(int(acceler)/2)+"*"+"x**2"+"+"+str(distance))
            elif dis_on == False:
                if (acceler and veloc) == ("" or " "):
                    distance_expre = 0; raise ValueError("No Value Given For Distance")
                elif veloc != ("" or " ") and acceler == ("" or " "):
                    distance_expre = sy.sympify(veloc+"*"+"x")
                elif veloc != ("" or " ") and acceler != ("" or " "):
                    distance_expre = sy.sympify(str(int(acceler)/2)+"*"+"x**2"+"+"+veloc+"*"+"x")
                elif veloc == ("" or " ") and acceler != ("" or " "):
                    distance_expre = sy.sympify(str(int(acceler)/2)+"*"+"x**2")
            x_points = []; y_points = []
            for i in range(50):
                if dis_sub_off:
                    x_points.append(i); y_points.append(distance_expre)
                elif dis_sub_off == False:
                    x_points.append(i); y_points.append(distance_expre.subs(x, i))
            plt.plot(x_points, y_points, linestyle='-'); plt.xlabel("Time(s)"); plt.ylabel("Distance(m)"); plt.show()
        except Exception, e:
            print("Failed To Graph data: "+str(e))
            self.result_area_buffer.set_text("I'm Sorry, distance\n Can't be Graphed, make sure you\n typed everything correctly ")

    def entry_sweeper(self):
        '''sweeps the entrys so that
        the other functions will work'''
        accel = self.acceleration_entry.get_text()
        veloc = self.velocity_entry.get_text()
        distance = self.distance_entry.get_text()
        if len(accel) == 0:
            self.acceleration_entry.set_text(" ")
        if len(veloc) == 0:
            self.velocity_entry.set_text(" ")
        if len(distance) == 0:
            self.distance_entry.set_text(" ")

        
  
            


        