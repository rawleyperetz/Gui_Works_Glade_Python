# from msilib.schema import Error
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
import caesarCipher
import socket 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@Gtk.Template(filename="FWindow.ui")
class FirstWindow(Gtk.Window):
    __gtype_name__= "FWindow"

    user = Gtk.Template.Child("user_entry")
    port = Gtk.Template.Child("port_entry")
    combo = Gtk.Template.Child("combo_combo")
    
    def __init__(self):
        Gtk.Window.__init__(self, title="EncryptionChatTCP")
        self.set_border_width(10)
        self.set_size_request(200,100)

        self.let_button = Gtk.Template.Child("button_button")
        
        store = Gtk.ListStore(str)
        ciphers = ["Caesar Cipher", "Vigenere Cipher", "RSA"]
        for cip in ciphers:
            store.append([cip])
        
        
        self.combo.set_model(store)
        self.combo.connect("changed", self.do_something_combo)
        renderer_text = Gtk.CellRendererText()
        self.combo.pack_start(renderer_text, True)
        self.combo.add_attribute(renderer_text, "text", 0)
        
        self.combo.set_active(0)

        self.init_template()
        
    @Gtk.Template.Callback()
    def do_something_combo(self, combo):
        print(self.combo.get_active())
        return combo.get_active_iter()
        

    @Gtk.Template.Callback()
    def let_button_clicked(self, widget):
        self.user_val = self.user.get_text()
        self.port_val = int(self.port.get_text())
        if self.user_val == '' or self.port_val == '':
            print('All Fields must be filled')
        try:
            client_socket.bind((socket.gethostname(), self.port_val))
            client_socket.listen()
        except:
            print(f'Shit I encountered an error')
        window.destroy()
        swindow = ChatWindow()
        swindow.connect("delete-event",Gtk.main_quit)
        swindow.show()

##############################################
#Second window
##############################################
@Gtk.Template(filename="SWindow.ui")
class ChatWindow(Gtk.Window):
    __gtype_name__= "SWindow"

    chat = Gtk.Template.Child("chat_entry")
    send = Gtk.Template.Child("send_button")
    txt_one = Gtk.Template.Child("txt_one_view")
    txt_two = Gtk.Template.Child("txt_two_view")

    def __init__(self):
        Gtk.Window.__init__(self, title="EncryptionChatTCP_Window")
        self.set_border_width(20)
        self.set_size_request(600,500)
        self.msg = ""
        self.init_template()
    
        incoming_msg = client_socket.recv(50)
        if incoming_msg != '':
            self.txt_one.get_buffer().set_text(incoming_msg+"\n")
            self.txt_two.get_buffer().set_text(">" + "\n")
    
    @Gtk.Template.Callback()
    def send_button_clicked(self,widget):
        chat_txt = self.chat.get_text()
        client_socket.send(caesarCipher.caesarEncrypt(chat_txt,3))
        self.msg = self.msg + '> ' + chat_txt + "\n"
        self.txt_two.get_buffer().set_text(self.msg)
        self.txt_one.get_buffer().set_text(caesarCipher.caesarEncrypt(self.msg,3)+"\n")
        if chat_txt == 'exit':
            client_socket.close()
            print("Wir sind fertig")
            Gtk.main_quit()
    
    @Gtk.Template.Callback()
    def exit_button_clicked(self, widget):
        Gtk.main_quit()
        

##############################################
#Runtime Part
##############################################
window = FirstWindow()
window.connect("delete-event",Gtk.main_quit)

window.show()

Gtk.main()