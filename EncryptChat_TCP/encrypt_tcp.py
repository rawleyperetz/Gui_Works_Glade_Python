# from msilib.schema import Error
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
import caesarCipher
import socket 
from time import sleep
import sys
import errno
import threading 


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
        print(self.user_val, 'and', self.port_val)
        # print(type(self.user_val), 'and', type(self.port_val))
        if self.user_val == '' or self.port_val == '':
            print('All Fields must be filled')
        #try:
        
        client_socket.bind(('', self.port_val))
        client_socket.listen(1)
        global cs
        cs, address = client_socket.accept()
        print('Connection established with {}'.format(str(address[0])))
        # sleep(10)
        # #except Exception as e:
        # print(f'Shit I encountered an error ')
        window.destroy()
        swindow = ChatWindow()
        swindow.connect("delete-event",Gtk.main_quit)
        swindow.show()
        sleep(30)
        swindow.run()
        
        
        
 
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
        self.old_caesar = ""
        self.init_template()
        # print()
        # try:
        #     incoming_msg = client_socket.recv(50)
        #     if incoming_msg != '':
        #         self.txt_one.get_buffer().set_text(incoming_msg+"\n")
        #         self.txt_two.get_buffer().set_text(">" + "\n")
        # except:
        #     print('Not connected')

    @Gtk.Template.Callback()
    def send_button_clicked(self, widget):
        try:
            self.chat_txt = self.chat.get_text()
            if self.chat_txt == 'exit':
                cs.close()
                print("Wir sind fertig")
                Gtk.main_quit()
            # client_socket.send(self.txt_one.get_text())
            self.msg = self.msg + '> ' + self.chat_txt + "\n"
            self.txt_two.get_buffer().set_text(self.msg)
            caesar = caesarCipher.caesarEncrypt(self.chat_txt,3)
            self.old_caesar = self.old_caesar + caesar + "\n"
            self.txt_one.get_buffer().set_text(self.old_caesar+"\n")
            #client_socket.send(bytes(caesarCipher.caesarEncrypt(chat_txt,3), "utf-8"))
            cs.send(bytes(caesar,'utf-8'))
        except Exception as e:
            print('Error occurred: {}'.format(str(e)))
            cs.close()
            sys.exit()
    
    @Gtk.Template.Callback()
    def exit_button_clicked(self, widget):
        Gtk.main_quit()
    
    def receiving(self):
        while True:
            try:    
                rmsg = cs.recv(20).decode('utf-8') #inc_header = cs.recv(20)
                # msg_len = int(inc_header.decode('utf-8').strip())
                # msg = cs.recv(msg_len).decode('utf-8')
                #print('shut up')
                if rmsg != '':
                    self.msg = self.msg + rmsg + "\n"
                    self.old_caesar = self.old_caesar + rmsg + "\n"
                    self.txt_one.get_buffer().set_text(self.old_caesar+"\n")
                    self.txt_two.get_buffer().set_text(">" + self.msg + "\n")

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error:{}'.format(str(e)))
                    sys.exit()
                continue

            except Exception as e:
                print('Reading error2:{}'.format(str(e)))
                sys.exit()
    
    def run(self):
        thread = threading.Thread(daemon=True, target=self.receiving)#, args=[self.in_seconds])
        thread.start()
        

##############################################
#Runtime Part
##############################################
window = FirstWindow()
window.connect("delete-event",Gtk.main_quit)

window.show()



Gtk.main()
