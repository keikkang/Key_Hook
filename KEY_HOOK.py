from urllib.request import AbstractBasicAuthHandler
import keyboard
import threading
import pyautogui
import socket #For Network Programming
import time
import queue #for queue messagea
import key_map

SERVER_IP = '192.168.0.83'
SERVER_PORT = 80 #DEFAULT HTTP PORT
STR_BUFFER = '  _COMMAND'
thread_off_flag = False
thread_on_flag = False
data_q = queue.Queue()

class Data_Frame:
    def __init__(self):
        self.data_key
    

class Hotkey(threading.Thread):
    def __init__(self):
        super(Hotkey, self).__init__()  # parent class __init__ 실행
        self.daemon = True  # for daemon  thread
        self.event_f4 = False  
        self.event_f5 = False 
        keyboard.unhook_all()  
        keyboard.add_hotkey('f4', print, args=['\nf4 was pressed'])  # f4가 눌리면 print 실행
        keyboard.add_hotkey('f5', print, args=['\nf5 was pressed'])  # f4가 눌리면 print 실행
        
    def run(self):  # run method override
        global thread_off_flag
        global thread_on_flag
        print('Hooking Started')
        while True:
            key = keyboard.read_hotkey(suppress=False)  # hotkey를 계속 읽음
            
            if key == 'f4':  # f4 받은 경우
                self.event_f4 = True  # event 클래스 변수를 True로 설정
                thread_on_flag = True

            if key == 'f5':
                self.event_f5 = True
                thread_off_flag = True
                break 
            
class Key_Hook(threading.Thread):
    def __init__(self):
        super(Key_Hook, self).__init__()  
        self.daemon = True  
    def run(self):
        while True:
            track_key = keyboard.read_key()
            data_q.put(track_key)
            #position_mouse = pyautogui.position()    
            print(f"Pressed_key: {track_key}")
            #print(f'\r{position_mouse.x:5}, {position_mouse.y:5}')
            time.sleep(0.05)
            if thread_off_flag == True :
                break
        
             
class My_Socket(threading.Thread):
    def __init__(self, ip_address, ip_port):
        super(My_Socket,self).__init__()
        self.Daemon = True
        self.ip_address = ip_address
        self.ip_port = ip_port
      
    def socket_create(self):
        self.nuvoton_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #SOCk_STERAM : TCP  / SOCk_DGRAM : UDP
        print("Socket Create OK")
        
    def socket_connect(self): 
        try:
            self.nuvoton_socket.connect((self.ip_address, self.ip_port))
            print("Socket Connect Ok")
        except:
            print("Socket Connect Fail")
    def socket_set_timeout(self, duration):
        self.nuvoton_socket.settimeout(duration)
    
    def send_message(self, value):
        #self.nuvoton_socket.send(value.encode())
        self.nuvoton_socket.send(value)
        
    def recv_message(self):
        return self.nuvoton_socket.recv(1024)
    
    def run(self):
        print("TCP/IP CLIENT START")
        self.socket_create()
        self.socket_connect()
        self.socket_set_timeout(0.5)     
        while True:
            if data_q.qsize()>=1:
                self.send_data = data_q.get()
                print(f'Data_val 1 : {self.send_data}')
                self.send_data = Get_Key(self.send_data)
                print(f'Data_val : {self.send_data}')
                self.send_str = f'{self.send_data}{STR_BUFFER.encode()}'
                self.send_message(self.send_str)
                time.sleep(1)
                self.data = self.recv_message()
                print("resp from server : {}".format(self.data))
                time.sleep(1)
            if thread_off_flag == True :
                break
            
def Get_Key(t_key): 
    for key, value in key_map.key_map.items():
        if t_key == key:
            return value
    
            
def Do_it():

    hotkey_thread = Hotkey() 
    hotkey_thread.start()  
    while True:
        if(hotkey_thread.event_f4) == True:   
            tcp_thread = My_Socket(SERVER_IP,SERVER_PORT)
            tcp_thread.start()
            hooking_thread = Key_Hook()
            hooking_thread.start()
            hotkey_thread.event_f4 = False
        if(hotkey_thread.event_f5) == True:
            break   
    tcp_thread.join()
    hotkey_thread.join()
    hooking_thread.join()
    keyboard.unhook_all()
    print("FINISH")
    
Do_it()  