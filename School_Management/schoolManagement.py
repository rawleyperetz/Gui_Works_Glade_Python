# Rawley Amankwah
# Importing necessary libraries
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio
import sqlite3
import sys


# Initializing ui children 
# Remember gtype name and ui template class name should be equal
# all function should be the same as the pressed handler in the ui
@Gtk.Template(filename="./SchManage_HomeWin.ui")
class FirstWindow(Gtk.Window):
    __gtype_name__= "Erste" #SchManage_HomeWin"

    fname = Gtk.Template.Child("FName")
    lname = Gtk.Template.Child("LName")
    dob = Gtk.Template.Child("dobID")
    class_room = Gtk.Template.Child("classID")
    home_add = Gtk.Template.Child("HomeID")
    teacher = Gtk.Template.Child("teacherID")
    guardian = Gtk.Template.Child("guardID")
    stud_id = Gtk.Template.Child("studID")
    
    #Entries
    fnameEnt = Gtk.Template.Child("FNameEntry")
    lnameEnt = Gtk.Template.Child("LNameEntry")
    dobEnt = Gtk.Template.Child("dobEntry")
    classEnt = Gtk.Template.Child("classEntry")
    homeEnt = Gtk.Template.Child("homeEntry")
    teacherEnt = Gtk.Template.Child("teacherEntry")
    guardianEnt = Gtk.Template.Child("guardianEntry")
    studEnt = Gtk.Template.Child("studEntry")

    searchEntry = Gtk.Template.Child("sEntry")
    
    def __init__(self):
        Gtk.Window.__init__(self, title="School Management System")
        # self.set_border_width(10)
        # self.set_size_request(200,100)
        #self.set_default_size()

        self.add_data = Gtk.Template.Child("insID")
        self.clear_data = Gtk.Template.Child("clID")
        self.display_data = Gtk.Template.Child("displayButton")

        # self.connector = sqlite3.connect('schStudent.db')
        # #global c
        # self.c = self.connector.cursor()
        self.init_template()  # initializing template
        

    @Gtk.Template.Callback()
    def addPressed(self, widget):
        # self. = self.user.get_text()
        # self.port_val = int(self.port.get_text())

        # get_text() - self explanatory
        self.fVal = self.fnameEnt.get_text()
        self.lVal = self.lnameEnt.get_text()
        self.dVal = self.dobEnt.get_text()
        self.cVal = self.classEnt.get_text()
        self.hVal = self.homeEnt.get_text()
        self.tVal = self.teacherEnt.get_text()
        self.gVal = self.guardianEnt.get_text()
        self.sVal = self.studEnt.get_text()
        
        # since id is unique, we need to check this
        if self.sVal =="":
            print("Student ID can not be empty")
            sys.exit()
        
        #checking existence
        connector = sqlite3.connect('schStudent.db')
        #global c
        c = connector.cursor()
        sqlite_check = """SELECT * FROM studentDB WHERE studentID=?;"""
        self.check_result = c.execute(sqlite_check,(self.sVal,)).fetchone() # fetchone return only one object in this case it is student id is unique 
        
        # if already exist, delete
        if self.check_result:
            sql_check_delete_query="""DELETE FROM studentDB WHERE studentID=?;"""
            c.execute(sql_check_delete_query,(self.sVal,))
            connector.commit()

        # update or add
        sqlite_insert_with_param = """INSERT INTO studentDB VALUES (?,?,?,?,?,?,?,?);"""
        data_tuple = (self.sVal,self.fVal,self.lVal,self.dVal,self.cVal,self.hVal,self.tVal,self.gVal)
        c.execute(sqlite_insert_with_param,data_tuple)
        connector.commit()
        print("Added Successfully")
        connector.close()

        self.clearFields(widget) # clear fields after adding
        #c.close()

    # clear all fields
    @Gtk.Template.Callback()
    def clearFields(self,widget):
        self.fnameEnt.set_text("")
        self.lnameEnt.set_text("")
        self.dobEnt.set_text("")
        self.classEnt.set_text("") 
        self.homeEnt.set_text("") 
        self.teacherEnt.set_text("") 
        self.guardianEnt.set_text("") 
        self.studEnt.set_text("") 
        
    # show database window
    @Gtk.Template.Callback()
    def dispPressed(self,button):

        #window.destroy()
        swindow = DisplayWindow()
        #swindow.connect("delete-event",Gtk.main_quit)
        swindow.show()
        #sleep(30)
        #swindow.run()
    
    # enter value in the search entry widget at the bottom left to get all entries for the stud id entry in the database
    # these entries would be filled in the entry fields
    @Gtk.Template.Callback()
    def upPressed(self,button):
        connector = sqlite3.connect('schStudent.db')
        #global c
        c = connector.cursor()
        self.search_entry_value = self.searchEntry.get_text()
        sql_search_query = """SELECT * FROM studentDB WHERE studentID=?;"""
        self.search_result = c.execute(sql_search_query,(self.search_entry_value,)).fetchone()
        entry_list = [self.studEnt,self.fnameEnt,self.lnameEnt,self.dobEnt,self.classEnt,self.homeEnt,self.teacherEnt,self.guardianEnt]
        for i,entry in enumerate(entry_list):
            entry.set_text(str(self.search_result[i]))
        
        connector.commit()
        connector.close()
        

    # self-explanatory
    @Gtk.Template.Callback()
    def delPressed(self,button):
        connector = sqlite3.connect('schStudent.db')
        #global c
        c = connector.cursor()
        self.search_entry_value = self.searchEntry.get_text()
        sql_delete_query="""DELETE FROM studentDB WHERE studentID=?;"""
        
        c.execute(sql_delete_query,(self.search_entry_value,))
        connector.commit()
        print('Entry Deleted')
        connector.close()
    
    # def on_destroy(self, widget):
    #     connector.close()
    #     self.connect("delete-event", Gtk.main_quit)
        # self.quit()
        # Gtk.main_quit()
        # sys.exit()
    
        
        
        
 
# ##############################################
# #Second window
# ##############################################
@Gtk.Template(filename="display_sch.ui")
class DisplayWindow(Gtk.Window):
    __gtype_name__= "DisplayWindow" 
    #connector.close()
    connector = sqlite3.connect('schStudent.db')
    #global c
    c = connector.cursor()
    all_data = c.execute("SELECT * FROM studentDB")
    db_list = all_data.fetchall()#c.execute("SELECT * FROM studentDB")
    
    # window scroll
    scroll_win = Gtk.Template.Child("win_scroll")

    # tree view
    treeView = Gtk.Template.Child("treeID")
    connector.commit()
    connector.close()

    # database display
    def __init__(self):
        Gtk.Window.__init__(self, title="School Management Database")
        self.db_liststore = Gtk.ListStore(int,str,str,str,str,str,str,str)

        for row in self.db_list:
            self.db_liststore.append(list(row))
        # column names of the treeView, i prefer student id first
        for i,column_title in enumerate(["Student ID","FirstName","LastName","DateOfBirth","ClassRoom","HomeAddress","Teacher","Guardian"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text =i)
            self.treeView.append_column(column)
        self.treeView.set_model(self.db_liststore)
        self.set_size_request(800,300)
        self.show_all() # doesn't seem important but no way i am deleting

    # I am not sure if this method works though, but imma leave it here
    def on_destroy(self, widget):
        #connector.close()
        Gtk.main_quit()
        #self.hide()
        
##############################################
#Runtime Part
##############################################
window = FirstWindow()
window.connect("delete-event",Gtk.main_quit)
window.show()

Gtk.main()