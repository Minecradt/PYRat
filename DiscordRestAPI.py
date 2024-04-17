import requests,threading,time,sys,base64,random
from json import dumps
api_url = "https://discord.com/api/v9" #api
def ListenCommand(profile,command,function,channel,arg_count,ignore_id):
    while True:
        message = profile.Message.LastMessage(profile,channel)
        if message:
            if (message['content'].split(' ')[0]==command) & (message['author']['id']!=ignore_id):
                #print('Stop',command)
                args = message['content'].split(' ')
                del args[0]
                if arg_count>=0:
                    args = args[:arg_count]
                #print(tuple(args))
                try:
                    #threading.Thread(target=function,args=tuple(args)).start()
                    function(*tuple(args))
                except:
                    pass

        global stop_threads
        try:
            stop_threads
        except:
            stop_threads = False
        if stop_threads:
            break
        time.sleep(random.uniform(0.4,5))
#classes
class TokenError(Exception):
    pass
class Functions:
    def StopThreads(self):
        global stop_threads
        stop_threads = True
    def __init__(self,token: str,bot: bool,bot_id:str):
        self.token: str = token
        self.headers: dict = {"Authorization":f"{['Bearer','Bot'][bot]} {token}",
"User-Agent":"myBotThing (http://some.url, v0.1)",
"Content-Type":"application/json", }
        self.bot_id: str = bot_id
    class Channel:
        def Create(profile,guild:str,name:str,parent=None):
            res = requests.post(
            f"{api_url}/guilds/{guild}/channels",
            json={
                "name": name,
                "type": 0,
                "permission_overwrites": [],
                "parent_id":parent
            },
            headers=profile.headers
            )
            return res.json()
        def Delete(profile,channel):
            return requests.delete(f"{api_url}/channels/{channel}",headers=profile.headers).json()
    class Message:
        def Send(profile,message:str,channel:str):
            POSTedJSON =  dumps ( {"content":message} )
            baseURL = "https://discordapp.com/api/channels/{}/messages".format(channel)
            req = requests.post(baseURL, headers = profile.headers, data = POSTedJSON)
            return req.json()
        def Reply(profile,message:str,guild_id,message_id,channel_id):
            POSTedJSON =  dumps ( {"content":message, "message_reference":{"message_id":message_id,"guild_id":guild_id,"channel_id":channel_id}} ) 
            baseURL = "https://discordapp.com/api/channels/{}/messages".format(channel_id)
            req = requests.post(baseURL, headers = profile.headers, data = POSTedJSON)
            return req.json()
        def LastMessage(profile,channel):
            try:
                return requests.get(f'{api_url}/channels/{channel}/messages?limit=1',headers=profile.headers).json()[0]
            except:
                return None
    class Command:
        def add_command(profile,command:str,channel,prefix,function,argcount:int = 0):
            cmd_thread = threading.Thread(target=ListenCommand,args=(profile,prefix + command,function,channel,argcount,profile.bot_id))
            cmd_thread.daemon = True
            cmd_thread.start()
class User:
    def __init__(self):
        self.token = None
    def Login(self,token: str,bot: bool):
        if requests.get('https://discord.com/api/v9/users/@me',headers={ 
            "Authorization":f"{['Bearer','Bot'][bot]} {token}",
            "User-Agent":"myBotThing (http://some.url, v0.1)",
            "Content-Type":"application/json", }).status_code==401:
            raise TokenError('Token "' + token + '" is Invalid!')
        else:
            if not bot:
                raise Warning('You can get banned if you use a user token!')
            bot_id = base64.b64decode(token.split('.')[0].encode() +  b'=' * (-len(token.split('.')[0].encode()) % 4)).decode()            
            return Functions(token,bot,bot_id)